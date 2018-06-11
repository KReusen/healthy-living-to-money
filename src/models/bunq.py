from typing import NamedTuple, Union

class PaymentInfo(NamedTuple):
    amount_string: str
    description: str
    to_iban: str
    from_iban: str

    def to_dict(self) -> dict:
        return self._asdict()