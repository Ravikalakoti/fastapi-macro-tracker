from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class User(Base):
	__tablename__ = "users"
	id = Column(Integer, primary_key=True, index=True)
	username = Column(String, unique=True)
	hashed_password = Column(String)

class Food(Base):
	__tablename__ = "foods"
	id = Column(Integer, primary_key=True, index=True)
	name = Column(String, unique=True, index=True)
	fat = Column(Float)
	protein = Column(Float)
	carbs = Column(Float)

class Meal(Base):
	__tablename__ = "foods"
	id = Column(Integer, primary_key=True, index=True)
	user_id = Column(Integer, ForeignKey=("users.id"))
	name = Column(String)
	user = relationship("user")
