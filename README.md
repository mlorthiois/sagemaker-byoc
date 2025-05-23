# Custom SageMaker-BYOC Image

This repository serves as a template for creating your Bring-Your-Own-Container (BYOC) for a SageMaker Endpoint.

## Customize

The 2 primary functions you'll likely modify are located in [src/inference_handler.py](./src/inference_handler.py). 

- `default_model_fn`: This function is responsible for loading model artifacts stored in the `model_dir` directory (which contains the contents of your `model.tar.gz` file).
- `default_predict_fn` This function has access to both data and models, and it executes your inference code.

In this template, `default_model_fn` loads two models (representing two functions that transform input data). 
`default_predict_fn` then runs the transformation with both models and concatenates the results.

You can modify `pyproject.toml` to add any other dependencies your project requires.

## Test

First, populate `artefact/model` with your model artifacts. This directy will be mounted in 
`model_dir` by default when the container runs. 

Next, create and run the image with the following command:

```sh
make up
```

Then, modify or create files in `tests/` directory. These files will serve as the payloads for 
your test requests.

You can call your server with : 

```sh
make predict # payload defaults to tests/payload.json
make predict PAYLOAD="tests/payload_2.json"
make predict PAYLOAD="tests/payload.csv" CONTENT_TYPE="text/csv"
```
