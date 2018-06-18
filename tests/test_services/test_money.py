import pytest

from services.money import PaymentProvider, PaymentDescriptionNotImplemented
from services.multiplier import BasicRunMultiplier

from models.workout import Run
from models.payment_info import PaymentInfo

from exceptions.money import PaymentDescriptionNotImplemented

@pytest.fixture
def dummy_run():
    return Run(
        id=1, 
        distance=2.35, 
        calories=1, 
        duration=2, 
        start_time=1, 
        burgers_burned=5, 
    )

@pytest.fixture
def dummy_multiplier():
    return BasicRunMultiplier()

class TestPaymentProvider:

    def test_create_payment_description(self, dummy_run):
        expected = "Because you ran 2.35 km!"
        payment_provider = PaymentProvider()
        result = payment_provider.create_payment_description("2.35", dummy_run)
        assert result == expected

    def test_create_payment_description_unknown_model(self):
        payment_provider = PaymentProvider()
        with pytest.raises(PaymentDescriptionNotImplemented):
            payment_provider.create_payment_description("2.35", "abc")

    def test_create_amount_string(self, dummy_run, dummy_multiplier) -> str:
        expected = "2.35"
        payment_provider = PaymentProvider()
        result = payment_provider.create_amount_string(dummy_run, dummy_multiplier)
        assert result == expected
