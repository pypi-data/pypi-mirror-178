from pipeline import (
    PipelineFile,
    pipeline_function,
    pipeline_model,
)
from cloudpickle import load as pickle_load
from torch import tensor
from torch.jit import load as torchscript_load


@pipeline_model
class TorchPickleModel:
    def __init__(self):
        self.model = None

    @pipeline_function(run_once=True, on_startup=True)
    def load(self, model_file: PipelineFile) -> bool:
        try:
            self.model = pickle_load(open(model_file.path, "rb"))
            self.model.eval()
            return True
        except Exception as e:
            print(e)
            return False

    @pipeline_function
    def predict(self, input_list: list) -> list:
        input_tensor = tensor(input_list)
        return self.model(input_tensor).tolist()


@pipeline_model
class TorchModel:
    def __init__(self):
        self.model = None

    @pipeline_function(run_once=True, on_startup=True)
    def load(self, model_file: PipelineFile) -> bool:
        try:
            self.model = torchscript_load(model_file.path)
            self.model.eval()
            return True
        except Exception as e:
            print(e)
            return False

    @pipeline_function
    def predict(self, input_list: list) -> list:
        input_tensor = tensor(input_list)
        return self.model(input_tensor).tolist()
