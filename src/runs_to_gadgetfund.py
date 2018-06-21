import os
import rollbar
from typing import List

from services.money import PaymentProvider
from services.multiplier import BasicMultiplier
from services.banking import BunqService
from services.endomondo import EndomondoService

from managers.parameter import ParameterManager
from managers.s3 import S3Manager

from models.workout import Run

RUNS_BUCKET_NAME = os.environ.get('RUNS_BUCKET')
PARAMETER_MANAGER = ParameterManager()

rollbar_key = PARAMETER_MANAGER.get('/rollbar/key')
rollbar.init(rollbar_key, 'runs-to-gadgetfund')

@rollbar.lambda_function
def handler(event, context):
    s3_manager = S3Manager(RUNS_BUCKET_NAME, 'runs.csv', Run)
    endomondo_service = EndomondoService()
    
    if s3_manager.has_entries_online():
        runs = endomondo_service.get_runs(5)
        max_id_in_s3 = s3_manager.get_max_int()
    else:
        runs = endomondo_service.get_runs(999)
        max_id_in_s3 = 0

    runs_to_upload = [r for r in runs if r.get_id() > max_id_in_s3 ]
    if runs_to_upload:
        config = {
            "bank_service": BunqService(),
            "from_iban": PARAMETER_MANAGER.get('/bunq/from_iban'),
            "to_iban": PARAMETER_MANAGER.get('/bunq/to_iban'),
            "multiplier": BasicMultiplier()
        }
        payment_provider = PaymentProvider(config)
        payment_provider.pay_out(runs_to_upload)
        s3_manager.append(runs_to_upload)

if __name__ == "__main__":
    handler(None, None)
