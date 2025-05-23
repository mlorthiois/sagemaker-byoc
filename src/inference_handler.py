from typing import Callable, TypeAlias, override
import numpy as np
import numpy.typing as npt
from sagemaker_inference import decoder, encoder
from sagemaker_inference.default_inference_handler import DefaultInferenceHandler

Array: TypeAlias = npt.NDArray[np.float64]
Model: TypeAlias = Callable[[Array], Array]
Models: TypeAlias = tuple[Model, Model]


def my_model(x: Array) -> Array:
    return x * 2


def my_model_2(x: Array) -> Array:
    return x**2


class InferenceHandler(DefaultInferenceHandler):
    """This class handles the whole lifecyle of model and input data."""

    @override
    def default_model_fn(self, model_dir: str, context: None = None) -> Models:
        """Loads a model.
        Users should provide customized model_fn() in script.

        Args:
            model_dir: a directory where model is saved.
            context (obj): the request context (default: None).

        Returns: A PyTorch model.
        """
        return (my_model, my_model_2)

    @override
    def default_input_fn(self, input_data, content_type, context):
        """A default input_fn that can handle JSON, CSV and NPZ formats.

        Args:
            input_data: the request payload serialized in the content_type format
            content_type: the request content_type
            context (obj): the request context (default: None).

        Returns: input_data deserialized in np.array.
        """
        return decoder.decode(input_data, content_type)

    @override
    def default_predict_fn(
        self, data: Array, model: Models, context: None = None
    ) -> Array:
        """A default predict_fn for PyTorch. Calls a model on data deserialized in input_fn.
        Runs prediction on GPU if cuda is available.

        Args:
            data: input data (np.array) for prediction deserialized by input_fn
            model: model(s) loaded in memory by default_model_fn
            context (obj): the request context (default: None).

        Returns: a prediction
        """
        pred1 = model[0](data)
        pred2 = model[1](data)
        return np.concatenate([pred1, pred2])

    @override
    def default_output_fn(self, prediction, accept, context=None):
        """Serializes predictions from predict_fn to JSON, CSV or NPY format.

        Args:
            prediction: a prediction result from predict_fn
            accept: type which the output data needs to be serialized
            context (obj): the request context (default: None).

        Returns: output data serialized
        """
        return encoder.encode(prediction, accept)
