from cerebrium.pipeline import (
    _generate_pipeline,
    _check_pipeline_type,
    CerebriumPipeline,
    ModelType,
    PrebuiltModelTypes
)
from cerebrium.errors import CerebriumRequestError

from pipeline import PipelineCloud
import requests
import json
import re
import os
from typing import Union, Tuple

from numpy import ndarray
from torch import Tensor


env = os.getenv("DEVELOPMENT_ENV", "prod")
if env == "dev":
    print("Using development environment")
    BASE_CEREBRIUM_URL = "https://dev-inference.cerebrium.ai"
else:
    BASE_CEREBRIUM_URL = "https://inference.cerebrium.ai"

REGEX_NAME_PATTERN = "^[A-Za-z0-9-]*$"


def _pipeline_string(pipeline: CerebriumPipeline):
    """
    Convert a pipeline to a string.

    Args:
        pipeline (CerebriumPipeline): The pipeline to convert.

    Returns:
        str: The pipeline as a string.
    """
    string = ""
    for i, component in enumerate(pipeline):
        val = component[0].value
        string += val
        if i != len(pipeline) - 1:
            string += "->"
    return string


def _check_auth_request(api_key: str) -> bool:
    """
    Check that the user is authenticated, returning the pipeline token if they are.

    Args:
        api_key (str): The API key for the Cerebrium account.
    Returns:
        dict ('status_code': int, 'data': dict): The response code and data. 'data' contains the pipeline token if successful.
    """

    url = f"{BASE_CEREBRIUM_URL}/getExternalApiKey"
    payload = {}
    headers = {"Authorization": api_key}

    response = requests.request(
        "POST", url, headers=headers, data=json.dumps(payload), timeout=10
    )
    data = {} if not response.text else json.loads(response.text)
    return {"status_code": response.status_code, "data": data}


def _register_model_request(
    name: str,
    pipeline_id: str,
    model_pipeline: CerebriumPipeline,
    description: str,
    api_key: str,
) -> str:
    """
    Register a model with Cerebrium.

    Args:
        pipeline_id (str): The ID of the pipeline to register.
        model_pipeline (CerebriumPipeline): The model pipeline.
        api_key (str): The API key for the Cerebrium account.

    Returns:
        dict ('status_code': int, 'data': dict): The response code and data. 'data' contains the endpoint of the registered model if successful.
    """

    url = f"{BASE_CEREBRIUM_URL}/models"
    payload = {
        "arguments": {
            "name": name,
            "externalId": pipeline_id,
            "modelType": _pipeline_string(model_pipeline),
        }
    }
    if description != "":
        payload["description"] = description
    headers = {"Authorization": api_key}

    response = requests.request(
        "POST", url, headers=headers, data=json.dumps(payload), timeout=30
    )
    return {"status_code": response.status_code, "data": json.loads(response.text)}

def _register_modal_model_request(
    name: str,
    model_id: str,
    model_pipeline: CerebriumPipeline,
    description: str,
    api_key: str,
) -> str:
    """
    Register a Modal model with Cerebrium. This is used for all prebuilt models

    Args:
        pipeline_id (str): The ID of the pipeline to register.
        model_pipeline (CerebriumPipeline): The model pipeline.
        api_key (str): The API key for the Cerebrium account.

    Returns:
        dict ('status_code': int, 'data': dict): The response code and data. 'data' contains the endpoint of the registered model if successful.
    """

    url = f"{BASE_CEREBRIUM_URL}/pre-built-model"
    payload = {
        "arguments": {
            "name": name,
            "externalId": model_id,
            "modelType": _pipeline_string(model_pipeline),
        }
    }
    if description != "":
        payload["description"] = description
    headers = {"Authorization": api_key}

    response = requests.request(
        "POST", url, headers=headers, data=json.dumps(payload), timeout=30
    )
    return {"status_code": response.status_code, "data": json.loads(response.text)}


def _convert_input_data(data: Union[list, ndarray, Tensor]) -> list:
    """
    Convert the input data to a list.

    Args:
        data (Union[list, ndarray, Tensor]): The data to convert.

    Returns:
        list: The converted data as a python list.
    """

    if isinstance(data, ndarray) or isinstance(data, Tensor):
        return data.tolist()
    else:
        return data


def model_api_request(
    model_endpoint: str,
    data: Union[list, ndarray, Tensor],
    api_key: str,
) -> dict:
    """
    Make a request to the Cerebrium model API.

    Args:
        model_endpoint (str): The endpoint of the model to make a request to.
        data (list): The data to send to the model.

    Returns:
        dict ('status_code': int, 'data': dict): The response code and data.
    """

    payload = _convert_input_data(data)
    headers = {"Authorization": api_key}
    response = requests.request(
        "POST", model_endpoint, headers=headers, data=json.dumps(payload), timeout=30
    )
    return {"status_code": response.status_code, "data": json.loads(response.text)}


def deploy(
    model_pipeline: CerebriumPipeline,
    pipeline_name: str,
    api_key: str,
    description: str = "",
    dry_run=False,
) -> str:
    """
    Deploy a model to Cerebrium.

    Args:
        model_pipeline (CerebriumPipeline): The pipeline to deploy. This is a list of ModelType and model path pairs, as such:
            [(ModelType.TORCH, "model.pt")]
        pipeline_name (str): The name to deploy the pipeline under.
        api_key (str): The API key for the Cerebrium account.
        description (str): An optional description of the model or pipeline.
        dry_run (bool): Whether to run the deployment in dry-run mode.
            If True, the model will not be deployed, and deploy will return a pipeline function which can be used to test with.

    Returns:
        str: The newly deployed REST endpoint. If dry_run is True, a pipeline function will be returned instead.
    """

    # Check that the model type is supported
    model_pipeline = _check_pipeline_type(model_pipeline)

    # Check that the pipeline name is valid
    if len(pipeline_name) > 20:
        raise ValueError("Pipeline name must be less than 20 characters")
    if not bool(re.match(REGEX_NAME_PATTERN, pipeline_name)):
        raise ValueError(
            "Pipeline name can only contain alphanumeric characters and hyphens"
        )

    # Check that the user is authenticated
    if not dry_run:
        check_auth_response = _check_auth_request(api_key)
        if check_auth_response["status_code"] != 200:
            raise CerebriumRequestError(
                check_auth_response["status_code"],
                "getExternalApiKey",
                check_auth_response["data"],
            )
        else:
            pipeline_token = check_auth_response["data"]["apiKey"]
    
    # Check if prebuilt requested
    if model_pipeline[0][0] == ModelType.PREBUILT:
        if dry_run:
            raise NotImplementedError("Dry run not supported for prebuilt models")
        else:
            model_id = model_pipeline[0][1]
            print("Registering with Cerebrium...")
            model_response = _register_modal_model_request(
                pipeline_name, model_id, model_pipeline, description, api_key
            )
            if model_response["status_code"] != 200:
                raise CerebriumRequestError(
                    model_response["status_code"], "models", model_response["data"]
                )
            else:
                endpoint = model_response["data"]["internalEndpoint"]
                print(f"Model {pipeline_name} deployed at {endpoint}")
                return endpoint
    else:
        # Create the pipeline
        pipeline = _generate_pipeline(pipeline_name, model_pipeline)

        if not dry_run:
            # Deploy the pipeline to PipelineAI and register the model with Cerebrium
            pipeline_cloud = PipelineCloud(token=pipeline_token, verbose=False)
            print("Uploading pipeline...")
            uploaded_pipeline = pipeline_cloud.upload_pipeline(pipeline)
            print("Registering with Cerebrium...")
            model_response = _register_model_request(
                pipeline_name, uploaded_pipeline.id, model_pipeline, description, api_key
            )
            if model_response["status_code"] != 200:
                raise CerebriumRequestError(
                    model_response["status_code"], "models", model_response["data"]
                )
            else:
                endpoint = model_response["data"]["internalEndpoint"]
                print(f"Model {pipeline_name} deployed at {endpoint}")
                return endpoint
        else:
            print("Dry run complete")

            def run_function(input_data):
                return pipeline.run(_convert_input_data(input_data))

            return run_function
