from tortoise.models import Model
from tortoise import fields
from tortoise import run_async

from database import init

class TestModel(Model):
    test = fields.IntField(null=False,
                           description=f"Test value")

    ts = fields.IntField(null=False,
                         description=f"Epoch time")

    def __str__(self):
        return f"Test: {self.test} Time: {self.ts}"


if __name__ == "__main__":
    run_async(init())