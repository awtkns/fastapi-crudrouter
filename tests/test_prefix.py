import pytest

from tests.implementations import implementations, BaseImpl


@pytest.fixture(params=implementations)
def router(request):
    impl: BaseImpl = request.param
    settings = {**impl.get_settings()[0], **dict(prefix=None)}
    router = impl.get_router()(**settings)

    yield router


def test_prefix_lowercase(router):
    assert type(router.prefix) is str
    assert router.prefix != ""
    assert router.prefix == router.prefix.lower()
