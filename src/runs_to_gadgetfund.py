import os
import rollbar

from services.parameter import ParameterService
from managers.endomondo import Endomondo
from managers.s3 import S3Manager
from models.run import Run

RUNS_BUCKET_NAME = os.environ.get('RUNS_BUCKET')
PARAMETER_SERVICE = ParameterService()

# rollbar_key = PARAMETER_SERVICE.get('/rollbar/key')
# rollbar.init(rollbar_key, 'runs-to-gadgetfund')

# @rollbar.lambda_function
def handler(event, context):
    s3_manager = S3Manager(RUNS_BUCKET_NAME, 'runs.csv', Run)
    
    if s3_manager.has_entries_online():
        max_runs_to_get = 5
    else:
        max_runs_to_get = 9999

    endomondo = Endomondo()
    runs = endomondo.get_runs(max_runs_to_get)

    max_id_in_s3 = s3_manager.get_max_int()
    


if __name__ == "__main__":
    handler(None, None)