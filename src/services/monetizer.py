from typing import List, Optional

from managers.bunq import BunqManager

from services.parameter import ParameterService

from models.workout import Run
from models.bunq import PaymentInfo

class RunsToMoney():
    def __init__(self):
        self.bunq_manager = BunqManager()
        self.parameter_service = ParameterService()
    
    def pay_out_runs(self, runs: List[Run]):
        multiplier = BasicMultiplier()
        payment_jobs = self._create_payment_jobs(runs, multiplier)
        for payment_job in payment_jobs:
            # self.bunq_manager.make_payment(payment_job)
            print(payment_job)
        
    def _create_payment_jobs(self, runs: List[Run], multiplier: object) -> List[PaymentInfo]:
        from_iban = self.parameter_service.get('/bunq/from_iban')
        to_iban = self.parameter_service.get('/bunq/to_iban')
        
        payment_jobs = []
        for run in runs:
            payment_jobs.append(
                PaymentInfo(
                    amount_string = multiplier.get_amount(run),
                    description = f'Because you ran {run.get_rounded_distance()} km!',
                    to_iban = to_iban,
                    from_iban = from_iban
                )
            )
        return payment_jobs

class BasicMultiplier():
    def __init__(self):
        self.multiply_by = 1
    
    def get_amount(self, run: object) -> str:
        return str(round(run.distance * self.multiply_by, 2))