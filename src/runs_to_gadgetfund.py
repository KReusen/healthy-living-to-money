import os
import rollbar
from services.parameter import ParameterService

RUNS_BUCKET = os.environ.get('RUNS_BUCKET')
PARAMETER_SERVICE = ParameterService()

# rollbar_key = PARAMETER_SERVICE.get('/rollbar/key')
# rollbar.init(rollbar_key, 'runs-to-gadgetfund')

# @rollbar.lambda_function
def handler(event, context):
    print(event)


if __name__ == "__main__":
    handler(None, None)