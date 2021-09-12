def test_version():
    import fastapi_crudrouter

    assert type(fastapi_crudrouter.__version__) is str


def test_version_file():
    from fastapi_crudrouter import _version

    assert type(_version.__version__) is str
