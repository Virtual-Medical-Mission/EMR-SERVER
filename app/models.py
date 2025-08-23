from enum import Enum
from pydantic import BaseModel

class Gender(str, Enum):
    male = "male"
    female = "female"

class Patient(BaseModel):
    id: int
    name: str
    age: int
    gender: Gender
    