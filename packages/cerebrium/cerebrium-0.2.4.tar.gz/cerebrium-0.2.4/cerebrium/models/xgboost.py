from pipeline import (
    PipelineFile,
    pipeline_function,
    pipeline_model,
)
from xgboost import XGBClassifier, XGBRegressor
from numpy import atleast_2d


@pipeline_model
class XGBClassifierModel:
    def __init__(self):
        self.model = None

    @pipeline_function(run_once=True, on_startup=True)
    def load(self, model_file: PipelineFile) -> bool:
        try:
            self.model = XGBClassifier()
            self.model.load_model(model_file.path)
        except Exception as e:
            print(e)
            return False

    @pipeline_function
    def predict(self, input_list: list) -> list:
        array = atleast_2d(input_list)
        return self.model.predict_proba(array).tolist()


@pipeline_model
class XGBRegressorModel:
    def __init__(self):
        self.model = None

    @pipeline_function(run_once=True, on_startup=True)
    def load(self, model_file: PipelineFile) -> bool:
        try:
            self.model = XGBRegressor()
            self.model.load_model(model_file.path)
            return True
        except Exception as e:
            print(e)
            return False

    @pipeline_function
    def predict(self, input_list: list) -> list:
        array = atleast_2d(input_list)
        return self.model.predict(array).tolist()
