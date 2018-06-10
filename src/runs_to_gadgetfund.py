import os
import rollbar
from services.parameter import ParameterService
from managers.endomondo import Endomondo
from managers.s3 import S3RunsManager

RUNS_BUCKET_NAME = os.environ.get('RUNS_BUCKET')
PARAMETER_SERVICE = ParameterService()

# rollbar_key = PARAMETER_SERVICE.get('/rollbar/key')
# rollbar.init(rollbar_key, 'runs-to-gadgetfund')

# @rollbar.lambda_function
def handler(event, context):
    s3_runs_manager = S3RunsManager(RUNS_BUCKET_NAME)
    
    if s3_runs_manager.file_has_entries():
        max_runs_to_get = 5
    else:
        max_runs_to_get = 500


    # endomondo = Endomondo()
    # runs = endomondo.get_runs(1)

    


if __name__ == "__main__":
    handler(None, None)