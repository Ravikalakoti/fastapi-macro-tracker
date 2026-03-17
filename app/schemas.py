from pydantic import BaseModel, constr

# ----------------
# User schemas
# ----------------
class UserBase(BaseModel):
    username: constr(min_length=3, max_length=50)

class UserCreate(UserBase):
    password: constr(min_length=6, max_length=72)  # bcrypt-safe

class UserOut(UserBase):
    id: int
    model_config = {"from_attributes": True}

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