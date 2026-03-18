from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

# Many-to-many relationship table between Meal and Food
meal_food_table = Table(
    "meal_food",
    Base.metadata,
    Column("meal_id", ForeignKey("meals.id"), primary_key=True),
    Column("food_id", ForeignKey("foods.id"), primary_key=True),
)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=True)
    full_name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    meals = relationship("Meal", back_populates="user")

class Food(Base):
    __tablename__ = "foods"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    fat = Column(Float, default=0.0)
    protein = Column(Float, default=0.0)
    carbs = Column(Float, default=0.0)
    meals = relationship("Meal", secondary=meal_food_table, back_populates="foods")

class Meal(Base):
    __tablename__ = "meals"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    user = relationship("User", back_populates="meals")
    timestamp = Column(DateTime, default=datetime.utcnow)
    foods = relationship("Food", secondary=meal_food_table, back_populates="meals")

    # --------- Macros properties ---------
    @property
    def total_fat(self):
        return sum(food.fat for food in self.foods)

    @property
    def total_protein(self):
        return sum(food.protein for food in self.foods)

    @property
    def total_carbs(self):
        return sum(food.carbs for food in self.foods)