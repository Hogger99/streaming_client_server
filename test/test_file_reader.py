import pytest
from src.file_reader import read_yaml_file

@pytest.fixture
def test_valid_file():
    return "test/test_data.yml"

@pytest.fixture
def test_invalid_file():
    return "test_invalid_data.yml"





def test_read_yaml_file(test_valid_file):
    contents = read_yaml_file(test_valid_file)
    assert contents == {'KEY1': 'value1', 'KEY2': 'value2'}


def test_read_yaml_file_invalid_file(test_invalid_file):
    contents = read_yaml_file(test_invalid_file)
    assert contents == f"error {test_invalid_file} does not exist"