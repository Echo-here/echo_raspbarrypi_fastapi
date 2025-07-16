from pydantic import BaseModel

class Order(BaseModel):
    sugar: float
    water: float
    coffee: float
    icetea: float
    greentea: float
