from pydantic import EmailStr, BaseModel, Field


class UserInSchema(BaseModel):
    """Модель пользователя без id"""
    name: str = Field(..., max_length=25, min_length=3, title='Задается name пользователя', pattern=r'^[a-zA-Z0-9_-]+$')
    second_name: str = Field(..., max_length=25, min_length=3, title='Задается second_name пользователя', pattern=r'^[a-zA-Z0-9_-]+$')
    email: EmailStr = Field(..., title='Задается email пользователя')
    password: str = Field(..., title='Задается пароль пользователя')


class UserSchema(UserInSchema):
    """Модель пользователя с id"""
    id: int



class OrderInSchema(BaseModel):
    """Модель заказа без id"""
    user_id: int = Field(..., title='Задается user_id пользователя')
    item_id: int = Field(..., title='Задается item_id товара')
    date: str = Field(..., title='Задается дата заказа')
    status: str = Field(..., title='Задается статус заказа')


class OrderSchema(OrderInSchema):
    """Модель заказа с id"""
    id: int



class ItemsInSchema(BaseModel):
    """Модель заказа без id"""
    title: str = Field(..., max_length=25, min_length=3, title='Задается наименование товара', pattern=r'^[a-zA-Z0-9_-]+$')
    description: str = Field(..., title='Задается описание товара')
    price: int = Field(..., title='Задается цена товара')


class ItemSchema(ItemsInSchema):
    """Модель товара с id"""
    id: int