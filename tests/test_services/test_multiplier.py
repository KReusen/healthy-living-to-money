import pytest

from services.multiplier import BasicMultiplier

from models.workout import Run
from models.body import Weights

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

def test_get_amount_with_run(dummy_run):
    m = BasicMultiplier()
    expected = 2.35
    result = m.get_amount(dummy_run)

    assert result == expected

def test_get_amount_with_run_times_10(dummy_run):
    m = BasicMultiplier(10)
    expected = 23.50
    result = m.get_amount(dummy_run)

    assert result == expected

def test_get_amount_with_weights(dummy_weights):
    m = BasicMultiplier()
    expected = -0.5
    result = m.get_amount(dummy_weights)

    assert result == expected
