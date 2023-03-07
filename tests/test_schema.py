from pydantic import BaseModel, Field
from fastapi_crudrouter.core._utils import schema_factory


class Onion(BaseModel):
    id: int = Field(primary_key=True)
    variety: str
    expire_on: str = Field(allow_mutation=False)

    class Config:
        validate_assignment = True


class TestAllowMutation:
    def test_schema_factory_update(self):
        """Field annotation allow_mutation=False are removed from schema."""
        schema = schema_factory(Onion, "Update")
        assert "variety" in schema.__fields__
        assert "expire_on" not in schema.__fields__
