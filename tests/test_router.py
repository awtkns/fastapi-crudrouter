from . import Potato

basic_potato = Potato(id=0, thickness=.24, mass=1.2, color='Brown', type='Russet')


def compare_dict(d1, d2, exclude: list = ['id']) -> bool:
    assert len(d1.keys()) == len(d2.keys())

    for key in d1.keys():
        if key not in exclude and d1[key] != d2[key]:
            return False

    return True



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

    assert compare_dict(res.json(), basic_potato.dict())


def test_update(client):
    res = client.post('/potato', json=basic_potato.dict())
    data = res.json()
    assert res.status_code == 200

    tuber = basic_potato.copy()
    tuber.type = 'tuber'
    tuber.mass = 5.5

    res = client.put(f'/potato/{data["id"]}', json=tuber.dict())
    assert res.status_code == 200
    assert compare_dict(res.json(), tuber.dict())
    assert not compare_dict(res.json(), basic_potato.dict())

    res = client.get(f'/potato/{data["id"]}')
    assert res.status_code == 200
    assert compare_dict(res.json(), tuber.dict())
    assert not compare_dict(res.json(), basic_potato.dict())


def test_delete_one(client):
    res = client.post('/potato', json=basic_potato.dict())
    data = res.json()
    assert res.status_code == 200

    res = client.get(f'/potato/{data["id"]}')
    assert res.status_code == 200
    assert compare_dict(res.json(), basic_potato.dict())

    res = client.delete(f'/potato/{data["id"]}')
    assert res.status_code == 200
    assert compare_dict(res.json(), basic_potato.dict())

    res = client.get('/potato')
    assert res.status_code == 200
    assert len(res.json()) == 0


def test_delete_all(client):
    res = client.post('/potato', json=basic_potato.dict())
    assert res.status_code == 200

    res = client.post('/potato', json=basic_potato.dict())
    assert res.status_code == 200

    assert len(client.get('/potato').json()) == 2

    res = client.delete('/potato')
    assert res.status_code == 200
    assert len(res.json()) == 0

    assert len(client.get('/potato').json()) == 0


def test_dne(client):
    res = client.get('/')
    assert res.status_code == 404

    res = client.get(f'/carrot')
    assert res.status_code == 404

