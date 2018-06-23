# 'https://www.googleapis.com/fitness/v1/users/me/dataSources/derived:com.google.weight:com.google.android.gms:merge_weight/datasets/0-1443194884000000000'
import os
import time
import rollbar

from managers.parameter import ParameterManager
from managers.s3 import S3Manager

from models.body import WeightEntry

HEALTH_DATA_BUCKET_NAME = os.environ.get('HEALTH_DATA_BUCKET_NAME')
PARAMETER_MANAGER = ParameterManager()

rollbar_key = PARAMETER_MANAGER.get('/rollbar/key')
rollbar.init(rollbar_key, 'runs-to-gadgetfund')

@rollbar.lambda_function
def handler(event, context):
    s3_manager = S3Manager(HEALTH_DATA_BUCKET_NAME, 'weights.csv', WeightEntry)
    current_nanos = get_current_nanos()
    min_nanos = 0

    if s3_manager.has_entries_online():
        min_nanos = s3_manager.get_max_int(column_name='startTimeNanos')

    

def get_current_nanos():
    return int(time.time()) * 1000000000