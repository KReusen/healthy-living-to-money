import pytest

from unittest.mock import ANY, patch

from services.money import PaymentProvider
from services.multiplier import BasicMultiplier

from models.workout import Run
from models.body import Weights
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
def dummy_weights():
    return Weights(
        old=80.5,
        new=80
    )

@pytest.fixture
def dummy_multiplier():
    return BasicMultiplier()

@pytest.fixture
def dummy_weight_multiplier():
    return BasicMultiplier(10)

@pytest.fixture
def dummy_config():
    return {
        "bank_service": None,
        "from_iban": 'from123',
        "to_iban": 'to123',
        "multiplier": BasicMultiplier()
    }

class TestPaymentProvider():


    def test_create_amount_from_and_to_ibans_run(self, dummy_run, dummy_multiplier, dummy_config) -> str:
        expected_amount_string = "2.35"
        expected_from_iban = "from123"
        expected_to_iban = "to123"

        payment_provider = PaymentProvider(dummy_config)
        amount_string, from_iban, to_iban = payment_provider.create_amount_from_and_to_ibans(dummy_run, dummy_multiplier)
        
        assert amount_string == expected_amount_string
        assert from_iban == expected_from_iban
        assert to_iban == expected_to_iban

    def test_create_amount_from_and_to_ibans_weightgain(self, dummy_weight_multiplier, dummy_config) -> str:
        weights = Weights(old=80, new=80.5)
        expected_amount_string = "5.0"
        expected_from_iban = "to123"
        expected_to_iban = "from123"

        payment_provider = PaymentProvider(dummy_config)
        amount_string, from_iban, to_iban = payment_provider.create_amount_from_and_to_ibans(weights, dummy_weight_multiplier)
        
        assert amount_string == expected_amount_string
        assert from_iban == expected_from_iban
        assert to_iban == expected_to_iban
    
    def test_create_amount_from_and_to_ibans_weightloss(self, dummy_weight_multiplier, dummy_config) -> str:
        weights = Weights(old=80.5, new=80)
        expected_amount_string = "5.0"
        expected_from_iban = "from123"
        expected_to_iban = "to123"

        payment_provider = PaymentProvider(dummy_config)
        amount_string, from_iban, to_iban = payment_provider.create_amount_from_and_to_ibans(weights, dummy_weight_multiplier)
        
        assert amount_string == expected_amount_string
        assert from_iban == expected_from_iban
        assert to_iban == expected_to_iban

    def test_create_payment_description_run(self, dummy_run, dummy_config, dummy_multiplier):
        expected = "Because you ran 2.35 km!"
        payment_provider = PaymentProvider(dummy_config)
        result = payment_provider.create_payment_description(dummy_run)
        assert result == expected

    def test_create_payment_description_unknown_model(self, dummy_config):
        payment_provider = PaymentProvider(dummy_config)
        with pytest.raises(PaymentDescriptionNotImplemented):
            payment_provider.create_payment_description("abc")

    def test_create_payment_description_weightloss(self, dummy_config, dummy_multiplier):
        weights = Weights(old=80.5, new=80)
        expected = "Because you lost 0.5 kg!"
        payment_provider = PaymentProvider(dummy_config)
        result = payment_provider.create_payment_description(weights)
        assert result == expected

    def test_create_payment_description_weightgain(self, dummy_config, dummy_multiplier):
        weights = Weights(old=80, new=80.5)
        expected = "Because you gained 0.5 kg!"
        payment_provider = PaymentProvider(dummy_config)
        result = payment_provider.create_payment_description(weights)
        assert result == expected

    def test_create_payment_info(self, dummy_config, dummy_run, dummy_multiplier):
        expected = PaymentInfo(
            amount_string='2.35',
            description='Because you ran 2.35 km!',
            from_iban='from123',
            to_iban='to123'
        )
        payment_provider = PaymentProvider(dummy_config)
        result = payment_provider.create_payment_info(dummy_run, dummy_multiplier)
        
        assert str(expected) == str(result)
