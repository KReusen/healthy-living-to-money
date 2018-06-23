import os
import pytest

from models.workout import Run

from managers.csv import CSVManager

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
def dummy_run2():
    return Run(
        id=2, 
        distance=5.35, 
        calories=20, 
        duration=10, 
        start_time=2, 
        burgers_burned=7, 
    )

@pytest.fixture
def csv_headers():
    return b'"id","distance","calories","duration","start_time","burgers_burned","speed_avg","speed_max","descent","ascent","altitude_max","altitude_min","hydration","heart_rate_avg","heart_rate_max"\r\n'

@pytest.fixture
def empty_csv_file_with_headers():
    file_name = 'empty.csv'

    with open(file_name, 'wb') as fh:
        fh.write(csv_headers())
    
    yield file_name

    try:
        os.remove(file_name)
    except OSError:
        pass


def test_create_empty_csv_body(dummy_run):
    expected = b'"id","distance","calories","duration","start_time","burgers_burned","speed_avg","speed_max","descent","ascent","altitude_max","altitude_min","hydration","heart_rate_avg","heart_rate_max"\r\n'
    result = CSVManager.create_empty_csv_body(dummy_run)
    assert result == expected

def test_append_to_file(empty_csv_file_with_headers, dummy_run, dummy_run2, csv_headers):
    filename = empty_csv_file_with_headers
    rows = [dummy_run, dummy_run2]
    data_model = Run

    CSVManager.append_to_file(filename, rows, data_model)

    with open(filename, 'rb') as fh:
        result = fh.read()
    
    assert result == b'"id","distance","calories","duration","start_time","burgers_burned","speed_avg","speed_max","descent","ascent","altitude_max","altitude_min","hydration","heart_rate_avg","heart_rate_max"\r\n1,2.35,1,2,1,5,,,,,,,,,\r\n2,5.35,20,10,2,7,,,,,,,,,\r\n'
    
