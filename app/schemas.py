from pydantic import BaseModel, constr, EmailStr
from typing import Optional

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

class MealCreate(MealBase):
    pass

class MealOut(MealBase):
    id: int
    model_config = {"from_attributes": True}