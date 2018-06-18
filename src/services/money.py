from typing import List, Optional

from services.banking import BunqService
from services.multiplier import BasicRunMultiplier

from managers.parameter import ParameterManager

from models.workout import Run
from models.payment_info import PaymentInfo

from exceptions.money import PaymentDescriptionNotImplemented
        
config = {
    "bank_service": BunqService(),
    "from_iban_parameter": '/bunq/from_iban',
    "to_iban_parameter": '/bunq/to_iban',
    "multiplier": BasicRunMultiplier()
}

class PaymentProvider():
    def __init__(self, config: dict = config):
        self.parameter_manager = ParameterManager()
        self.bank_service = config.get("bank_service")
        self.from_iban = self.parameter_manager.get(config.get("from_iban_parameter"))
        self.to_iban = self.parameter_manager.get(config.get("to_iban_parameter"))
        self.multiplier = config.get("multiplier")
    
    def pay_out(self, model: object, data: List[Run]):
        payment_jobs = self.create_payment_jobs(data, self.multiplier)
        for payment_job in payment_jobs:
            self.bank_service.make_payment(payment_job)
        
    # def create_payment_jobs(self, data: List[object], multiplier: object) -> List[PaymentInfo]:
    #     payment_jobs = []
    #     for entry in data:
    #         payment_jobs.append(
    #             PaymentInfo(
    #                 amount_string = multiplier.get_amount(entry),
    #                 description = f'Because you ran {entry.get_rounded_distance()} km!',
    #                 to_iban = self.to_iban,
    #                 from_iban = self.from_iban
    #             )
    #         )
    #     return payment_jobs
    

    def create_payment_jobs(self, data: List[object], multiplier: object) -> List[PaymentInfo]:
        pass
    
    def create_payment_info(self, datamodel: object, multiplier: object):
        amount_string = self.create_amount_string(datamodel, multiplier)
        description = self.create_payment_description(amount_string, datamodel)

    def create_payment_description(self, amount_string: str, datamodel: object):
        if isinstance(datamodel, Run):
            return f"Because you ran {datamodel.get_rounded_distance()} km!"
        
        raise PaymentDescriptionNotImplemented(f"Payment description not implemented yet for {datamodel} ")

    def create_amount_string(self, datamodel: object, multiplier: object) -> str:
        return multiplier.get_amount(datamodel)

