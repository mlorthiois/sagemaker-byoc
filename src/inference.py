from typing import Callable, TypeAlias
import numpy as np
import numpy.typing as npt
from sagemaker_inference import decoder, encoder
import joblib

Array: TypeAlias = npt.NDArray[np.float64]


class Model:
    @classmethod
    def predict_a(cls, x):
        return x * 2

    @classmethod
    def predict_b(cls, x):
        return x**2


def model_fn(model_dir: str, context: None = None) -> Model:
    """Loads a model.

    Args:
        model_dir: a directory where model is saved.
        context (obj): the request context (default: None).

    Returns: A PyTorch model.
    """
    model_path = f"{model_dir}/example.joblib"
    model = joblib.load(model_path)
    return model


def input_fn(input_data, content_type, context):
    """A function that can handle JSON, CSV and NPZ formats.

    Args:
        input_data: the request payload serialized in the content_type format
        content_type: the request content_type
        context (obj): the request context (default: None).

    Returns: input_data deserialized in np.array.
    """
    return decoder.decode(input_data, content_type)


def predict_fn(data: Array, model, context: None = None) -> Array:
    """Calls a model on data deserialized in input_fn.

    Args:
        data: input data (np.array) for prediction deserialized by input_fn
        model: model(s) loaded in memory by default_model_fn
        context (obj): the request context (default: None).

    Returns: a prediction
    """
    pred1 = model.predict_a(data)
    pred2 = model.predict_b(data)
    return np.concatenate([pred1, pred2])


def default_output_fn(prediction, accept, context=None):
    """Serializes predictions from predict_fn to JSON, CSV or NPY format.

    Args:
        prediction: a prediction result from predict_fn
        accept: type which the output data needs to be serialized
        context (obj): the request context (default: None).

    Returns: output data serialized
    """
    return encoder.encode(prediction, accept)
