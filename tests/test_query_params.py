from tests.test_router import test_post, test_get


def test_simple(client):
    test_post(client)
    test_post(client, expected_length=2)
    test_post(client, expected_length=3)

    basic_potato = dict(thickness=0.24, mass=1.2, color="Red", type="Mini")
    test_post(client, model=basic_potato, expected_length=1)

    data = test_get(client, params={'color': 'Red'})
    assert len(data) == 1, data


