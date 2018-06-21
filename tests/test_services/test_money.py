import pytest

from unittest.mock import ANY, patch

from services.money import PaymentProvider
from services.multiplier import BasicMultiplier

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
    return BasicMultiplier()

@pytest.fixture
def dummy_config():
    return {
        "bank_service": None,
        "from_iban_parameter": '/bunq/from_iban',
        "to_iban_parameter": '/bunq/to_iban',
        "multiplier": BasicMultiplier()
    }

@pytest.fixture
def dummy_parameter_manager():
    config = dummy_config()
    return {
        config["from_iban_parameter"]: config["from_iban_parameter"],
        config["to_iban_parameter"]: config["to_iban_parameter"]
    }

class TestPaymentProvider():

    @patch('services.money.ParameterManager')
    def test_create_payment_description(self, mock_parameter_manager, dummy_parameter_manager, dummy_run, dummy_config):
        mock_parameter_manager.return_value = dummy_parameter_manager
        expected = "Because you ran 2.35 km!"
        payment_provider = PaymentProvider(dummy_config)
        result = payment_provider.create_payment_description("2.35", dummy_run)
        assert result == expected

    @patch('services.money.ParameterManager')
    def test_create_payment_description_unknown_model(self, mock_parameter_manager, dummy_parameter_manager, dummy_config):
        mock_parameter_manager.return_value = dummy_parameter_manager
        payment_provider = PaymentProvider(dummy_config)
        with pytest.raises(PaymentDescriptionNotImplemented):
            payment_provider.create_payment_description("2.35", "abc")

    @patch('services.money.ParameterManager')
    def test_create_amount_string(self, mock_parameter_manager, dummy_run, dummy_multiplier, dummy_parameter_manager, dummy_config) -> str:
        mock_parameter_manager.return_value = dummy_parameter_manager
        expected = "2.35"
        payment_provider = PaymentProvider(dummy_config)
        result = payment_provider.create_amount_string(dummy_run, dummy_multiplier)
        assert result == expected
