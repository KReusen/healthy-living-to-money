import os
import rollbar
from services.parameter import ParameterService
from managers.endomondo import Endomondo

RUNS_BUCKET = os.environ.get('RUNS_BUCKET')
PARAMETER_SERVICE = ParameterService()

# rollbar_key = PARAMETER_SERVICE.get('/rollbar/key')
# rollbar.init(rollbar_key, 'runs-to-gadgetfund')

# @rollbar.lambda_function
def handler(event, context):
    endomondo = Endomondo()
    runs = endomondo.get_runs(1)

    


if __name__ == "__main__":
    handler(None, None)