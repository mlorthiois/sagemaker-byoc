FROM python:3.13-slim

LABEL com.amazonaws.sagemaker.capabilities.accept-bind-to-port=true

WORKDIR /usr/src/app

COPY pyproject.toml pyproject.toml

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get clean && \
    apt-get -y install --no-install-recommends \
      ca-certificates \
      openjdk-17-jre-headless \
      wget && \
    pip install --no-cache-dir .

COPY src src

ENTRYPOINT ["python", "/usr/src/app/src/entrypoint.py"]
