import pytest

from models.workout import Run
from utils.models import get_field_names_from_data_model, create_model_from_dict

@pytest.fixture
def dummy_run():
    return Run(
        id=1, 
        distance=2.35, 
        calories=1, 
        duration=2, 
        start_time=1, 
        burgers_burned=5
    )

def test_get_field_names_from_data_model(dummy_run):
    expected = ['id', 'distance', 'calories', 'duration', 'start_time', 'burgers_burned', 'speed_avg', 'speed_max', 'descent', 'ascent', 'altitude_max', 'altitude_min', 'hydration', 'heart_rate_avg', 'heart_rate_max']
    result = get_field_names_from_data_model(dummy_run)
    assert sorted(result) == sorted(expected)

def test_create_model_from_dict(dummy_run):
    d = dict(
        id=1, 
        distance=2.35, 
        calories=1, 
        duration=2, 
        start_time=1, 
        burgers_burned=5
    )

    result = create_model_from_dict(Run, d)
    assert str(result) == str(dummy_run)
