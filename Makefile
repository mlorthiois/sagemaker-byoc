up:
	@docker build -t sagemaker-inference-base . && \
		docker run \
			-p 8080:8080 \
			--mount type=bind,src=./artefact/example.joblib,dst=/opt/ml/model/example.joblib \
			-e SAGEMAKER_MODEL_SERVER_WORKERS=1 \
			sagemaker-inference-base

PAYLOAD = "tests/payload_2.json"
CONTENT_TYPE = application/json

predict:
	curl -s --data-binary @$(PAYLOAD) -H "Content-Type: $(CONTENT_TYPE)" -v http://localhost:8080/invocations
