import os
import rollbar
from typing import List

from services.parameter import ParameterService
from services.secret import SecretService

from managers.endomondo import Endomondo
from managers.s3 import S3Manager
from managers.bunq import BunqManager

from models.workout import Run
from models.bunq import PaymentInfo

RUNS_BUCKET_NAME = os.environ.get('RUNS_BUCKET')
PARAMETER_SERVICE = ParameterService()

# rollbar_key = PARAMETER_SERVICE.get('/rollbar/key')
# rollbar.init(rollbar_key, 'runs-to-gadgetfund')

# @rollbar.lambda_function
def handler(event, context):
    s3_manager = S3Manager(RUNS_BUCKET_NAME, 'runs.csv', Run)
    endomondo = Endomondo()
    
    if s3_manager.has_entries_online():
        runs = endomondo.get_runs(5)
        max_id_in_s3 = s3_manager.get_max_int()
    else:
        runs = endomondo.get_runs(9999)
        max_id_in_s3 = 0

    runs_to_upload = [r for r in runs if r.get_id() > max_id_in_s3 ]
    if runs_to_upload:
        # pay_out_runs(runs_to_upload)
        s3_manager.append(runs_to_upload)

def pay_out_runs(runs: List[Run]):
    bunq_manager = BunqManager()
    payment_jobs = create_payment_jobs_from_runs(runs)
    for payment_job in payment_jobs:
        bunq_manager.make_payment(payment_job)
    
def create_payment_jobs_from_runs(runs: List[Run], multiplier: int = 1) -> List[PaymentInfo]:
    from_iban = PARAMETER_SERVICE.get('/bunq/from_iban')
    to_iban = PARAMETER_SERVICE.get('/bunq/to_iban')
    
    payment_jobs = []
    for run in runs:
        payment_jobs.append(
            PaymentInfo(
                amount_string = str(round(run.distance * multiplier, 2)),
                description = f'Because you ran {run.get_rounded_distance()} km!',
                to_iban = to_iban,
                from_iban = from_iban
            )
        )
    return payment_jobs

if __name__ == "__main__":
    handler(None, None)
