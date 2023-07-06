import pytest
from src.file_reader import read_yaml_file, read_json_file

@pytest.fixture
def test_valid_yaml_file():
    return "test/test_data.yml"

@pytest.fixture
def test_invalid_yaml_file():
    return "test_invalid_data.yml"


@pytest.fixture
def test_valid_json_file():
    return "test/test_data.json"

@pytest.fixture
def test_invalid_json_file():
    return "test_invalid_data.json"





def test_read_yaml_file(test_valid_yaml_file):
    contents = read_yaml_file(test_valid_yaml_file)
    assert contents == {'KEY1': 'value1', 'KEY2': 'value2'}


def test_read_yaml_file_invalid(test_invalid_yaml_file):
    contents = read_yaml_file(test_invalid_yaml_file)
    assert contents == f"error {test_invalid_yaml_file} does not exist"


def test_read_json_file(test_valid_json_file):
    contents = read_json_file(test_valid_json_file)
    assert contents == {'KEY1': 'value1', 'KEY2': 'value2'}


def test_read_json_file_invalid(test_invalid_json_file):
    contents = read_json_file(test_invalid_json_file)
    assert contents == f"error {test_invalid_json_file} does not exist"