from typing import List, Optional, Tuple

from services.banking import BunqService
from services.multiplier import BasicMultiplier

from models.workout import Run
from models.body import Weights
from models.payment_info import PaymentInfo

from exceptions.money import PaymentDescriptionNotImplemented
        
config = {
    "bank_service": BunqService(),
    "from_iban": 'from123',
    "to_iban": 'to123',
    "multiplier": BasicMultiplier()
}

class PaymentProvider():
    def __init__(self, config: dict = config):
        self.bank_service = config.get("bank_service")
        self.from_iban = config.get("from_iban")
        self.to_iban = config.get("to_iban")
        self.multiplier = config.get("multiplier")
    
    def pay_out(self, data: List[object]):
        payment_jobs = self.create_payment_jobs(data, self.multiplier)
        for payment_job in payment_jobs:
            # self.bank_service.make_payment(payment_job)
            pass

    def create_payment_jobs(self, data: List[object], multiplier: object) -> List[PaymentInfo]:
        return [self.create_payment_info(datamodel, multiplier) for datamodel in data ]
    
    def create_payment_info(self, datamodel: object, multiplier: object):
        amount_string, from_iban, to_iban = self.create_amount_from_and_to_ibans(datamodel, multiplier)
        description = self.create_payment_description(datamodel)
        return PaymentInfo(
            amount_string=amount_string,
            description=description,
            from_iban=from_iban,
            to_iban=to_iban
        )

    def create_payment_description(self, datamodel: object):
        try:
            units = datamodel.payout_units()
        except AttributeError:
            raise PaymentDescriptionNotImplemented(f"Payment description not implemented yet for {datamodel} ")
        
        if isinstance(datamodel, Run):
            return f"Because you ran {units} km!"
        if isinstance(datamodel, Weights):
            if units < 0:
                return f"Because you lost {abs(datamodel.payout_units())} kg!"
            return f"Because you gained {abs(datamodel.payout_units())} kg!"

        raise PaymentDescriptionNotImplemented(f"Payment description not implemented yet for {datamodel} ")


    def create_amount_from_and_to_ibans(self, datamodel: object, multiplier: object) -> Tuple[str]:
        amount = multiplier.get_amount(datamodel)

        if isinstance(datamodel, Weights) and amount > 0:
            # reverse to and from ibans when weight was gained
            return (str(abs(amount)), self.to_iban, self.from_iban) 
        
        return (str(abs(amount)), self.from_iban, self.to_iban)
