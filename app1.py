import asyncio
from typing import List
from fastapi import FastAPI, HTTPException
import uvicorn
from database import startup, shutdown, db
from passlib.context import CryptContext
from asyncio import run
from sqlalchemy import select, delete, insert, update
from models import UserModel, OrderModel, ItemModel
from schemas import UserSchema, UserInSchema, OrderSchema, OrderInSchema, ItemSchema, ItemsInSchema
from tools import get_password_hash

#from app import app1

app1 = FastAPI()
#app.mount(path='/', app=app1)
app1.add_event_handler("startup", startup)
app1.add_event_handler("shutdown", shutdown)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@app1.get("/users/", response_model=List[UserSchema])
async def get_all_users() -> List[UserSchema]:
    """Получение списка всех пользователей: GET /users/"""
    query = select(UserModel)
    users = await db.fetch_all(query)
    if users:
        return users
    raise HTTPException(status_code=404, detail="Нет ни одного пользователя")


@app1.get('/users/{user_id}', response_model=UserSchema)
async def get_single_user(user_id: int) -> UserSchema:
    """Получение информации о конкретном пользователе: GET /users/{user_id}/"""
    query = select(UserModel).where(UserModel.id == user_id)
    db_user = await db.fetch_one(query)
    if db_user:
        return db_user
    raise HTTPException(status_code=404, detail="Пользователь не найден")


@app1.post('/users/', response_model=UserSchema)
async def create_user(user: UserInSchema) -> dict:
    """Создание нового пользователя: POST /users/"""
    hashed_password = await get_password_hash(user.password)
    user_dict = user.dict() #.model_dump()
    user_dict['password'] = hashed_password
    query = insert(UserModel).values(**user_dict)
    user_id = await db.execute(query, user_dict)
    return {**user_dict, 'id': user_id}


@app1.put('/users/{user_id}', response_model=UserSchema)
async def update_user(user_id: int, user: UserInSchema) -> UserSchema:
    """Обновление информации о пользователе: PUT /users/{user_id}/"""
    query = select(UserModel).where(UserModel.id == user_id)
    db_user = await db.fetch_one(query)
    if db_user:
        updated_user = user.dict(exclude_unset=True)
        if 'password' in updated_user:
            updated_user['password'] = await get_password_hash(updated_user.pop('password'))
        query = update(UserModel).where(UserModel.id == user_id).values(updated_user)
        await db.execute(query)
        return await db.fetch_one(select(UserModel).where(UserModel.id == user_id))
    raise HTTPException(status_code=404, detail="Пользователь не найден")


@app1.delete("/users/{user_id}")
async def delete_user(user_id: int) -> dict:
    """Удаление пользователя: DELETE /users/{user_id}/"""
    query = select(UserModel).where(UserModel.id == user_id)
    db_user = await db.fetch_one(query)
    if db_user:
        query = delete(UserModel).where(UserModel.id == user_id)
        await db.execute(query)
        return {'detail': f'Пользователь с id={db_user.id} удален'}
    raise HTTPException(status_code=404, detail="Пользователь не найден")


@app1.get("/orders/", response_model=List[OrderSchema])
async def get_all_users() -> List[OrderSchema]:
    """Получение списка всех заказов: GET /orders/"""
    query = select(OrderModel)
    order = await db.fetch_all(query)
    if order:
        return order
    raise HTTPException(status_code=404, detail="Нет ни одного заказа")


@app1.get('/orders/{order_id}', response_model=OrderSchema)
async def get_single_user(order_id: int) -> OrderSchema:
    """Получение информации о конкретном пользователе: GET /orders/{order_id}/"""
    query = select(OrderModel).where(OrderModel.id == order_id)
    db_order = await db.fetch_one(query)
    if db_order:
        return db_order
    raise HTTPException(status_code=404, detail="Заказ не найден")


@app1.post('/orders/', response_model=OrderSchema)
async def create_user(order: OrderSchema) -> dict:
    """Создание нового заказа: POST /orders/"""
    hashed_password = await get_password_hash(order.password)
    order_dict = order.dict() #.model_dump()
    order_dict['password'] = hashed_password
    query = insert(OrderModel).values(**order_dict)
    order_id = await db.execute(query, order_dict)
    return {**order_dict, 'id': order_id}


@app1.put('/orders/{order_id}', response_model=OrderSchema)
async def update_user(order_id: int, order: OrderInSchema) -> OrderSchema:
    """Обновление информации о пользователе: PUT /users/{order_id}/"""
    query = select(OrderModel).where(OrderModel.id == order_id)
    db_order = await db.fetch_one(query)
    if db_order:
        updated_order = order.dict(exclude_unset=True)
        if 'password' in updated_order:
            updated_order['password'] = await get_password_hash(updated_order.pop('password'))
        query = update(OrderModel).where(OrderModel.id == order_id).values(updated_order)
        await db.execute(query)
        return await db.fetch_one(select(OrderModel).where(OrderModel.id == order_id))
    raise HTTPException(status_code=404, detail="Заказ не найден")


@app1.delete("/orders/{order_id}")
async def delete_user(order_id: int) -> dict:
    """Удаление пользователя: DELETE /users/{order_id}/"""
    query = select(OrderModel).where(OrderModel.id == order_id)
    db_order = await db.fetch_one(query)
    if db_order:
        query = delete(OrderModel).where(OrderModel.id == order_id)
        await db.execute(query)
        return {'detail': f'Заказ с id={db_order.id} удален'}
    raise HTTPException(status_code=404, detail="Заказ не найден")

@app1.get("/items/", response_model=List[ItemSchema])
async def get_all_users() -> List[ItemSchema]:
    """Получение списка всех товаров: GET /items/"""
    query = select(ItemModel)
    items = await db.fetch_all(query)
    if items:
        return items
    raise HTTPException(status_code=404, detail="Нет ни одного товара")


@app1.get('/items/{item_id}', response_model=ItemSchema)
async def get_single_user(item_id: int) -> ItemSchema:
    """Получение информации о конкретном товаре: GET /items/{item_id}/"""
    query = select(ItemModel).where(ItemModel.id == item_id)
    db_item = await db.fetch_one(query)
    if db_item:
        return db_item
    raise HTTPException(status_code=404, detail="товар не найден")


@app1.post('/items/', response_model=ItemSchema)
async def create_user(item: ItemSchema) -> dict:
    """Создание нового товара: POST /orders/"""
    hashed_password = await get_password_hash(item.password)
    item_dict = item.dict() #.model_dump()
    item_dict['password'] = hashed_password
    query = insert(ItemModel).values(**item_dict)
    item_id = await db.execute(query, item_dict)
    return {**item_dict, 'id': item_id}


@app1.put('/items/{items_id}', response_model=ItemSchema)
async def update_user(item_id: int, item: ItemsInSchema) -> ItemSchema:
    """Обновление информации о товаре: PUT /items/{items_id}/"""
    query = select(ItemModel).where(ItemModel.id == item_id)
    db_item = await db.fetch_one(query)
    if db_item:
        updated_item = item.dict(exclude_unset=True)
        if 'password' in updated_item:
            updated_item['password'] = await get_password_hash(updated_item.pop('password'))
        query = update(ItemModel).where(ItemModel.id == item_id).values(updated_item)
        await db.execute(query)
        return await db.fetch_one(select(ItemModel).where(ItemModel.id == item_id))
    raise HTTPException(status_code=404, detail="Товар не найден")


@app1.delete("/items/{items_id}")
async def delete_user(item_id: int) -> dict:
    """Удаление товара: DELETE /items/{items_id}/"""
    query = select(ItemModel).where(ItemModel.id == item_id)
    db_item = await db.fetch_one(query)
    if db_item:
        query = delete(ItemModel).where(ItemModel.id == item_id)
        await db.execute(query)
        return {'detail': f'Товар с id={db_item.id} удален'}
    raise HTTPException(status_code=404, detail="Товар не найден")

if __name__ == "__main__":
    import asyncio
    asyncio.run(startup())

    async def preapereUser():
        query = delete(UserModel)
        await db.execute(query)
        query = insert(UserModel)
        for i in range(10):
            password = pwd_context.hash(f"password{i}")
            new_user = {"name": f"name{i}", "second_name": f"second_name{i}", "email": f"name{i}@mail.ru", "password": password}
            await db.execute(query, new_user)
        
    async def preapereOder():
        query = delete(OrderModel)
        await db.execute(query)
        query = insert(OrderModel)
        for i in range(10):
            new_order = {"user_id": i, "item_id": i, "date": f"{i}.12.20203", "status": "статус_{i}"}
            await db.execute(query, new_order)

    async def preapereItems():
        query = delete(ItemModel)
        await db.execute(query)
        query = insert(ItemModel)
        for i in range(10):
            new_item = {"title": f"title_{i}", "description": f"description_{i}", "price": i}
            await db.execute(query, new_item)
    
    asyncio.run(preapereUser())
    asyncio.run(preapereOder())
    asyncio.run(preapereItems())
    #run(preapereUser())
    #run(preapereOder())
    #run(preapereItems())
    #run("main:app", host='127.0.0.1', port=8000, reload=True)