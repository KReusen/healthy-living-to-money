from typing import List
from dataclasses import dataclass

from utils.models import get_field_names_from_data_model

@dataclass
class PaymentInfo:
    amount_string: str
    description: str
    to_iban: str
    from_iban: str

    def to_dict(self) -> dict:
        return self.__dict__
    
    def get_field_names(self) -> List[str]:
        return [key for key in self.__dict__ ]