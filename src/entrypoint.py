import subprocess
from subprocess import CalledProcessError
import service_handler
from retrying import retry
from sagemaker_inference import model_server

HANDLER_SERVICE = service_handler.__file__ + ":HandlerService:handle"


def _retry_if_error(exception):
    return isinstance(exception, CalledProcessError or OSError)


@retry(stop_max_delay=1000 * 50, retry_on_exception=_retry_if_error)
def _start_mms():
    # by default the number of workers per model is 1, but we can configure it through the
    # environment variable below if desired.
    # os.environ['SAGEMAKER_MODEL_SERVER_WORKERS'] = '2'
    print("Starting MMS -> running ", HANDLER_SERVICE)
    model_server.start_model_server(handler_service=HANDLER_SERVICE)


def main():
    _start_mms()
    # prevent docker exit
    subprocess.call(["tail", "-f", "/dev/null"])


main()
