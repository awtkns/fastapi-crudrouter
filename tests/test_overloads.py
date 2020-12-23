import pytest

URL = '/potato'
PARAMS = [-1, 0, 1, 14, 'ten']


def check_response(res):
    assert res.status_code == 200
    assert 'Overloaded' in res.text


def test_get_all(overloaded_client):
    check_response(overloaded_client.get(URL))


@pytest.mark.parametrize('id_', PARAMS)
def test_get_one(overloaded_client, id_):
    check_response(overloaded_client.get(f'{URL}/{id_}'))


def test_create(overloaded_client):
    check_response(overloaded_client.post(URL))


@pytest.mark.parametrize('id_', PARAMS)
def test_update(overloaded_client, id_):
    check_response(overloaded_client.put(f'{URL}/{id_}'))


@pytest.mark.parametrize('id_', PARAMS)
def test_delete(overloaded_client, id_):
    check_response(overloaded_client.delete(f'{URL}/{id_}'))


def test_delete_all(overloaded_client):
    check_response(overloaded_client.get(URL))
