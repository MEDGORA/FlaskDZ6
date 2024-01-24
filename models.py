from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UserModel(Base):
    """Таблица Users"""
    __tablename__ = 'users'
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String(length=50), unique=True, index=True)
    second_name = Column(String(length=50), unique=True, index=True)
    email = Column(String(length=50), unique=True, index=True)
    password = Column(String, nullable=False)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'User(id={self.id}, name={self.name}, second_name={self.second_name}, email={self.email})'
    
class OrderModel(Base):
    """Таблица Orders"""
    __tablename__ = 'oders'
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    user_id = Column(Integer, foreing_key = True, index=True)
    item_id = Column(Integer, foreing_key = True, index=True)
    date = Column(String(length=50),  index=True)
    status = Column(String(length=50),  index=True)

    def __str__(self):
        return self.date, self.status

    def __repr__(self):
        return f'Order(id={self.id}, user_id={self.user_id}, item_id={self.item_id}, date={self.date}, status={self.status}'   

class ItemModel(Base):
    """Таблица Items"""
    __tablename__ = 'items'
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    title = Column(String(length=50), unique=True, index=True)
    description = Column(String, unique=True, index=True)
    price = Column(Integer, index=True)

    def __str__(self):
        return self.title, self.description, self.price

    def __repr__(self):
        return f'Item(id={self.id}, title={self.title}, description={self.description}, price={self.price}'  