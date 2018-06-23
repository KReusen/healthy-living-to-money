# 'https://www.googleapis.com/fitness/v1/users/me/dataSources/derived:com.google.weight:com.google.android.gms:merge_weight/datasets/0-1443194884000000000'
import os
import time
import rollbar

from managers.parameter import ParameterManager
from managers.s3 import S3Manager
from managers.google_fit import WeightManager

from services.google_fit import GoogleFitService

from models.body import WeightEntry, Weights

HEALTH_DATA_BUCKET_NAME = os.environ.get('HEALTH_DATA_BUCKET_NAME')
MINIMUM_NANOS = os.environ.get('MINIMUM_NANOS', '1528917191000000000')
PARAMETER_MANAGER = ParameterManager()

rollbar_key = PARAMETER_MANAGER.get('/rollbar/key')
rollbar.init(rollbar_key, __file__)

@rollbar.lambda_function
def handler(event, context):
    s3_manager = S3Manager(HEALTH_DATA_BUCKET_NAME, 'weights.csv', WeightEntry)
    min_nanos = int(MINIMUM_NANOS)

    if s3_manager.has_entries_online():
        min_nanos = s3_manager.get_max_int(column_name='startTimeNanos')

    google_fit_service = GoogleFitService()
    access_token = google_fit_service.get_access_token()

    weight_manager = WeightManager(access_token)
    weights = weight_manager.get_weights(min_nanos)
