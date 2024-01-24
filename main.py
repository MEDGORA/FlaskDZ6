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

from app1 import app1

app = FastAPI()
app.mount(path='/', app=app)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


if __name__ == "__main__":
    uvicorn.run("main:app", host='127.0.0.1', port=8000, reload=False)
