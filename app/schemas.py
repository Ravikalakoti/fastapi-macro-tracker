from pydantic import BaseModel
from typing import Optional

#User schema
class UserBase(BaseModel):
	username: str

class UserCreate(UserBase):
	password: str

class UserOut(UserBase):
	id: int

	class config:
		orm_mode = True


#Food schema
class FoodBase(BaseModel):
	name: str
	fat: float
	protein: float
	carbs: float

class FoodCreate(FoodBase):
	pass

class FoodOut(FoodBase):
	id: int

	class config:
		orm_mode = True


#Meal schema
class MealBase(BaseModel):
	name: str
	user_id: int

class MealCreate(MealBase):
	pass

class MealOut(MealBase):
	id: int

	class Config:
		orm_mode = True








