from pipeline import Pipeline
from typing import Tuple, List
from enum import Enum
from types import FunctionType
from inspect import getsource


class ModelType(Enum):
    XGBOOST_CLASSIFIER = "xgboost_classifier"
    XGBOOST_REGRESSOR = "xgboost_regressor"
    TORCH = "torch"
    SKLEARN = "sklearn"
    SKLEARN_CLASSIFIER = "sklearn_classifier"
    ONNX = "onnx"
    SKLEARN_PREPROCESSOR = "sklearn_preprocessor"
    PREBUILT = "prebuilt"

CerebriumPipeline = List[Tuple[ModelType, str, FunctionType]]

PrebuiltModelTypes = [
    "mt0-xl",
    "galactica",
    "whisper-medium",
    "flan-xl"
]

def _get_function_arg(def_string) -> List[str]:
    """
    Return the arguments of a string function defition as a list of strings.

    Args:
        def_string: The string function definition line.

    Returns:
        A list of strings containing the arguments of the function.
    """
    argument_bracket_1 = def_string.find("(")
    argument_bracket_2 = def_string.find(")")
    argument_str = def_string[argument_bracket_1 + 1 : argument_bracket_2]
    return argument_str.split(",")


def _check_pipeline_type(model_pipeline: any) -> CerebriumPipeline:
    """
    Check if the given model_pipeline is a valid CerebriumPipeline.

    Args:
        model_pipeline: The model_pipeline to check.

    Returns:
        CerebriumPipeline: The model_pipeline if it is valid. Adds post-process and outer list of necessary.

    Raises:
        TypeError: If the model_pipeline is not a valid CerebriumPipeline.
    """
    if not isinstance(model_pipeline, list) and not isinstance(model_pipeline, tuple):
        raise TypeError(
            f"model_pipeline must be a tuple or list, but is {type(model_pipeline)}"
        )

    # If the model_pipeline is a list or tuple, check if all elements are tuples for single model pipeline
    if len(model_pipeline) == 2:
        if (
            not isinstance(model_pipeline[0], list)
            and not isinstance(model_pipeline[0], tuple)
            and not isinstance(model_pipeline[1], list)
            and not isinstance(model_pipeline[1], tuple)
        ):
            model_pipeline = [model_pipeline]
    elif len(model_pipeline) == 3:
        if (
            not isinstance(model_pipeline[0], list)
            and not isinstance(model_pipeline[0], tuple)
            and not isinstance(model_pipeline[1], list)
            and not isinstance(model_pipeline[1], tuple)
            and not isinstance(model_pipeline[2], list)
            and not isinstance(model_pipeline[2], tuple)
        ):
            model_pipeline = [model_pipeline]

    if model_pipeline[0][0] == ModelType.ONNX:
        if len(model_pipeline) != 1:
            raise TypeError(
                f"ONNX model_pipeline must be a tuple or list of length 1, but is {len(model_pipeline)}"
            )
    if model_pipeline[0][0] == ModelType.PREBUILT:
        if len(model_pipeline) != 1:
            raise TypeError(
                f"Prebuilt models must be a tuple or list of length 1, but is {len(model_pipeline)}"
            )
        if (model_pipeline[0][1] not in PrebuiltModelTypes):
            raise NotImplementedError(
                f"Prebuilt model {model_pipeline[0][1]} not found. Available models are {PrebuiltModelTypes}"
            )
        else:
            return model_pipeline

    for i, pipeline_component in enumerate(model_pipeline):
        model_type, model_filepath = pipeline_component[0], pipeline_component[1]
        if i > 0 and model_type == ModelType.ONNX:
            raise NotImplementedError(
                "ONNX models are currently only supported as single models in pipelines."
            )
        if i > 0 and model_type == ModelType.PREBUILT:
            raise NotImplementedError(
                "Prebuilt models are currently only supported as single models in pipelines."
            )
        if not isinstance(model_type, ModelType):
            raise TypeError(
                f"Model {i}: model_type must be of type ModelType, but is {type(model_type)}. Please ensure you use a valid Cerebrium typing."
            )
        if not isinstance(model_filepath, str):
            raise TypeError(
                f"Model {i}: model_filepath must be of type str, but is {type(model_filepath)}"
            )
        else:
            # Check valid file type
            if (
                not model_filepath.endswith(".pkl")
                and not model_filepath.endswith(".pt")
                and not model_filepath.endswith(".json")
                and not model_filepath.endswith(".onnx")
            ):
                raise TypeError(
                    f"Model {i}: model_filepath must be be a valid file type, but is {model_filepath}"
                )
        if len(pipeline_component) == 3:
            post_process = pipeline_component[2]
            if not isinstance(post_process, FunctionType):
                raise TypeError(
                    f"Model {i}: The post-processing function must be of type FunctionType, but is {type(post_process)}"
                )
            post_process_str = getsource(post_process).replace("\t", "    ").split("\n")
            post_process_args = _get_function_arg(post_process_str[0])
            if post_process_args[0] == "":
                post_process_args = []
            if len(post_process_args) != 1:
                raise NotImplementedError(
                    f"Model {i}: The post-processing function must have exactly one argument, but has {len(post_process_args)}"
                )

            contains_return = [s.strip()[:6] == "return" for s in post_process_str]
            if not any(contains_return):
                raise NotImplementedError(
                    f"Model {i}: The post-processing function must return a value, but does not."
                )

        else:
            model_pipeline[i] = (model_type, model_filepath, None)
    return model_pipeline


def _generate_pipeline(
    pipeline_name: str, pipeline: CerebriumPipeline, test_mode=False
) -> Pipeline:
    """
    Generate a Pipeline for the given CerebriumPipeline.

    Args:
        pipeline_name (str): The name of the pipeline.
        model_pipeline: The CerebriumPipeline to generate a Pipeline for.

    Returns:
        Pipeline: The generated pipeline.
    """
    # Imports
    pipeline_string = (
        "from pipeline import Pipeline, Variable, PipelineFile, pipeline_function\n"
        "from cerebrium.models.pickle import PickleModel, PickleClassifierModel, PicklePreprocessorModel\n"
        "from cerebrium.models.torch import TorchModel, TorchPickleModel\n"
        "from cerebrium.models.xgboost import XGBClassifierModel, XGBRegressorModel\n"
        "from cerebrium.models.onnx import OnnxModel\n"
        "from typing import Any\n\n"
    )

    # Define post-processing functions
    for i, (_, _, post_process) in enumerate(pipeline):
        if post_process:
            post_process_str = getsource(post_process).replace("\t", "    ").split("\n")
            argument_str = _get_function_arg(post_process_str[0])[0]
            pipeline_string += "@pipeline_function\n"
            pipeline_string += f"def post_process_{i}({argument_str}) -> Any:\n"
            pipeline_string += "    from numpy import ndarray\n"
            pipeline_string += "    from torch import Tensor\n"
            for line in post_process_str[1:]:
                if line != "" and line.strip()[0] != "#":
                    if line.strip()[:6] == "return":
                        pipeline_string += f"{line}\n\n"
                        break
                    else:
                        pipeline_string += f"{line}\n"

    # Start pipeline
    pipeline_string += (
        f"with Pipeline('{pipeline_name}') as pipeline:\n"
        "    input_data = Variable(type_class="
    )
    if pipeline[0][0] == ModelType.ONNX:
        pipeline_string += "dict, is_input=True)\n"
    else:
        pipeline_string += "list, is_input=True)\n"
    for i, (_, model_filepath, _) in enumerate(pipeline):
        pipeline_string += (
            f"    model_file_{i} = PipelineFile(path='./{model_filepath}')\n"
        )

    # Add pipeline variables
    pipeline_string += "    pipeline.add_variables(input_data,"
    for i in range(len(pipeline)):
        pipeline_string += f"model_file_{i},"
    pipeline_string += ")\n"

    # Add models
    for i, (model_type, model_filepath, _) in enumerate(pipeline):
        if model_filepath.endswith(".pkl"):
            if model_type == ModelType.TORCH:
                pipeline_string += f"    model_{i} = TorchPickleModel()\n"
            elif (
                model_type == ModelType.XGBOOST_CLASSIFIER
                or model_type == ModelType.SKLEARN_CLASSIFIER
            ):
                pipeline_string += f"    model_{i} = PickleClassifierModel()\n"
            elif (
                model_type == ModelType.XGBOOST_REGRESSOR
                or model_type == ModelType.SKLEARN
            ):
                pipeline_string += f"    model_{i} = PickleModel()\n"
            else:
                pipeline_string += f"    model_{i} = PicklePreprocessorModel()\n"
        elif model_type == ModelType.XGBOOST_CLASSIFIER:
            pipeline_string += f"    model_{i} = XGBClassifierModel()\n"
        elif model_type == ModelType.XGBOOST_REGRESSOR:
            pipeline_string += f"    model_{i} = XGBRegressorModel()\n"
        elif model_type == ModelType.TORCH:
            pipeline_string += f"    model_{i} = TorchModel()\n"
        elif model_type == ModelType.ONNX:
            pipeline_string += f"    model_{i} = OnnxModel()\n"
        else:
            # Assume pickled preprocessor file
            pipeline_string += f"    model_{i} = PicklePreprocessorModel()\n"

        pipeline_string += f"    model_{i}.load(model_file_{i})\n"

    # Add model predictions and post-processing
    pipeline_string += "    output_0 = model_0.predict(input_data)\n"
    if pipeline[0][2]:
        pipeline_string += "    output_0 = post_process_0(output_0)\n"

    for i in range(1, len(pipeline)):
        pipeline_string += f"    output_{i} = model_{i}.predict(output_{i-1})\n"

        if pipeline[i][2]:
            pipeline_string += f"    output_{i} = post_process_{i}(output_{i})\n"

    # End pipeline and execute
    pipeline_string += f"    pipeline.output(output_{len(pipeline)-1})\n"
    exec(pipeline_string)
    if test_mode:
        return Pipeline.get_pipeline(pipeline_name), pipeline_string
    else:
        return Pipeline.get_pipeline(pipeline_name)
