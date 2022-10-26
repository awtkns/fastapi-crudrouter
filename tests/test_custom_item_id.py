from . import test_router
from pytest import mark

from tests import CUSTOM_TAGS

potato_type = dict(name="russet", origin="Canada")

PATHS = ["/potato", "/carrot"]

class TestOpenAPISpec:
    def test_schema_exists(self, custom_item_id_client):
        res = custom_item_id_client.get("/openapi.json")
        assert res.status_code == 200

        return res

    @mark.parametrize("path", PATHS)
    def test_response_types(self, custom_item_id_client, path):
        schema = self.test_schema_exists(custom_item_id_client).json()
        paths = schema["paths"]

        for method in ["get", "post", "delete"]:
            assert "200" in paths[path][method]["responses"]

        assert "422" in paths[path]["post"]["responses"]

        if path == "/potato":
            item_path = path + "/{potato_id}"
        else:
            item_path = path + "/{carrot_id}"
        for method in ["get", "put", "delete"]:
            assert "200" in paths[item_path][method]["responses"]
            assert "404" in paths[item_path][method]["responses"]
            assert "422" in paths[item_path][method]["responses"]