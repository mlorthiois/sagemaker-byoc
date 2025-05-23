up:
	@docker build -t sagemaker-inference-base . && docker run -p 8080:8080 -v ./artefact:/opt/ml sagemaker-inference-base

PAYLOAD = "tests/payload.json"
CONTENT_TYPE = application/json

predict:
	curl -s --data-binary @$(PAYLOAD) -H "Content-Type: $(CONTENT_TYPE)" -v http://localhost:8080/invocations
