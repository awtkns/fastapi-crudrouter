from . import Potato

basic_potato = Potato(id=0, thickness=.24, mass=1.2, color='Brown', type='Russet')


def test_get(client):
    res = client.get('/potato')
    data = res.json()

    assert res.status_code == 200
    assert type(data) == list and len(data) == 0


def test_post(client):
    res = client.post('/potato', json=basic_potato.dict())
    assert res.status_code == 200

    data = client.get('/potato').json()
    assert len(data) == 1


def test_get_one(client):
    res = client.post('/potato', json=basic_potato.dict())
    assert res.status_code == 200

    data = client.get('/potato').json()
    assert len(data) == 1

    res = client.get(f'/potato/{data[0]["id"]}')
    assert res.status_code == 200
    assert res.json() == potato.dict()


def test_dne(client):
    res = client.get('/')
    assert res.status_code == 404

    res = client.get(f'/carrot')
    assert res.status_code == 404

