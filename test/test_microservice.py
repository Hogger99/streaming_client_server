import pytest
import src.microservice as ms

# make sure database is running when you do these tests
def test_query_relational_data():
    ms.config_file_name='../src/test_config.yml'

    query = ms.Query(**{'name':'stephen', 'key':None, 'age':None, 'value':None})

    records = ms.query_relational_data(query=query)
    assert len(records) == 1


def test_query_unstructured_data():
    ms.config_file_name='../src/test_config.yml'

    query = ms.Query(**{'name':'stephen', 'key':None, 'age':None, 'value':None})

    records = ms.query_unstructured_data(query=query)
    assert len(records) == 1



























