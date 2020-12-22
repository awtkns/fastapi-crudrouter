from pydantic import BaseModel


class Potato(BaseModel):
    id: int
    thickness: float
    mass: float
    color: str
    type: str
