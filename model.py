from pydantic import BaseModel

class Order(BaseModel):
    room: str
    name: str
    sugar: float
    water: float
    coffee: float
    icetea: float
    greentea: float
