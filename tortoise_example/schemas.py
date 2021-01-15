from model import TestModel
from flaxx.pydantic_schema_generator import pydantic_model_creator

TestSchema = pydantic_model_creator(TestModel, name=f"{TestModel.__name__}Schema")
TestSchemaCreate = pydantic_model_creator(TestModel, name=f"{TestModel.__name__}SchemaCreate",
                                          exclude_pk=True)
