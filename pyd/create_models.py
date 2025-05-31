from pydantic import BaseModel, Field
from typing import List



class CreateUser(BaseModel):
    surname: str = Field(example='Иванов', min_length=1, max_length=32)
    name: str = Field(example='Иван', min_length=1, max_length=32)
    # email: str = Field(example='ivan.ivanov@mail.ru', min_length=5, max_length=64)
    # login: str = Field(example='ivanych', min_length=1, max_length=32)
    password: str = Field(example='testpass', min_length=8, max_length=32)
    # role: int = Field(example=3, default=3)


class CreateRole(BaseModel):
    name: str = Field(example='customer', min_length=1, max_length=32)


class CreatePlant(BaseModel):
    name: str = Field(example='Азалия', min_length=1, max_length=32)
    desc: str = Field(example='Цветок с яркими цветами, популярен среди цветоводов.', min_length=1, max_length=1024)
    price: float = Field(example=250.0, gt=0.0)
    packing: int = Field(example=1, ge=1)
    category: int = Field(example=3)
    # seller: int = Field(example=1)
    image: str | None = Field(default=None)


class CreateCategory(BaseModel):
    name: str = Field(example='flowers', min_length=1, max_length=32)

class CreateReview(BaseModel):
    plant_id: int = Field(example=1, gt=0)
    review: str = Field(example='', min_length=1, max_length=4096)