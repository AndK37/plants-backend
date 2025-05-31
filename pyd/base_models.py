from pydantic import BaseModel, Field
from datetime import datetime



class BaseUser(BaseModel):
    id: int = Field(example=1)
    surname: str = Field(example='Иванов')
    name: str = Field(example='Иван')
    # email: str = Field(example='ivan.ivanov@mail.ru')
    login: str = Field(example='ivanych')
    # password: str = Field(example='testpass')


class BaseUserLogin(BaseModel):
    login: str = Field(example='ivanych')
    password: str = Field(example='testpass')


class BasePlant(BaseModel):
    id: int = Field(example=1)
    name: str = Field(example='Азалия')
    desc: str = Field(example='Цветок с яркими цветами, популярен среди цветоводов.')
    price: float = Field(example=250.0)
    packing: int = Field(example=1)
    image: str | None = Field( default=None, example='./img/plants/1.png')
    rating: float | None = Field(default=None, example=5.0)


class BaseRole(BaseModel):
    id: int = Field(example=1)
    name: str = Field(example='customer')


class BaseCategory(BaseModel):
    id: int = Field(example=1)
    name: str = Field(example='fruits')

class BaseFavorite(BaseModel):
    id: int = Field(example=1)

class BaseCart(BaseModel):
    id: int = Field(example=1)
    amount: int = Field(example=5)

class BaseReview(BaseModel):
    id: int = Field(example=1)
    plant_id: int = Field(example=1)
    review: str = Field(example='')
    upvotes: int = Field(example=1)

class BaseOrder(BaseModel):
    id: int = Field(example=1)
    amount: int = Field(example=1)
    date_of_order: datetime = Field(example='2025-05-05 10:10:10')
