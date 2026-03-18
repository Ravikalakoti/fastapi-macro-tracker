from pydantic import BaseModel, constr, EmailStr
from typing import Optional, List

# ----------------
# User schemas
class Token(BaseModel):
    access_token: str
    token_type: str 


class UserBase(BaseModel):
    username: constr(min_length=3, max_length=50)
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: constr(min_length=6, max_length=72)


class UserOut(UserBase):
    id: int

    model_config = {
        "from_attributes": True
    }

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[constr(min_length=6)] = None

    model_config = {
        "from_attributes": True
    }

# ----------------
# Food schemas
# ----------------
class FoodBase(BaseModel):
    name: str
    fat: float
    protein: float
    carbs: float

class FoodCreate(FoodBase):
    pass

class FoodOut(FoodBase):
    id: int
    model_config = {"from_attributes": True}

# ----------------
# Meal schemas
# ----------------
class MealBase(BaseModel):
    name: str
    user_id: int
    food_ids: List[int]

class MealCreate(BaseModel):
    name: str
    food_ids: List[int]

class MealOut(BaseModel):
    id: int
    name: str
    user_id: int
    foods: list[FoodOut]
    total_fat: float
    total_protein: float
    total_carbs: float

    model_config = {"from_attributes": True}