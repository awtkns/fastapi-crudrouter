from tests import CUSTOM_TAGS

POTATO_TAGS = ["Potato"]
PATH_TAGS = {
    "/potato": POTATO_TAGS,
    "/potato/{item_id}": POTATO_TAGS,
    "/carrot": CUSTOM_TAGS,
    "/carrot/{item_id}": CUSTOM_TAGS,
}


class TestOpenAPISpec:
    def test_schema_exists(self, client):
        res = client.get("/openapi.json")
        assert res.status_code == 200

        return res

    def test_schema_tags(self, client):
        schema = self.test_schema_exists(client).json()
        paths = schema["paths"]

        assert len(paths) == len(PATH_TAGS)
        for path, method in paths.items():
            assert len(method) == 3

            for m in method:
                assert method[m]["tags"] == PATH_TAGS[path]
