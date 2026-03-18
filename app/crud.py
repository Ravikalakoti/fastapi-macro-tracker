from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app import models, schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
MAX_BCRYPT_LENGTH = 72

# ---------------- User CRUD ----------------
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user(db: Session, user: schemas.UserCreate):
    password_bytes = user.password.encode("utf-8")[:MAX_BCRYPT_LENGTH]
    password_to_hash = password_bytes.decode("utf-8", errors="ignore")
    hashed_password = pwd_context.hash(password_to_hash)

    db_user = models.User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# ---------------- Food CRUD ----------------
def create_food(db: Session, food: schemas.FoodCreate):
    db_food = models.Food(**food.dict())
    db.add(db_food)
    db.commit()
    db.refresh(db_food)
    return db_food

def list_foods(db: Session):
    return db.query(models.Food).all()

# ---------------- Meal CRUD ----------------
def create_meal(db: Session, meal: schemas.MealCreate):
    db_meal = models.Meal(name=meal.name, user_id=meal.user_id)
    if meal.food_ids:
        foods = db.query(models.Food).filter(models.Food.id.in_(meal.food_ids)).all()
        db_meal.foods = foods
    db.add(db_meal)
    db.commit()
    db.refresh(db_meal)
    return db_meal

def list_user_meals(db: Session, user_id: int):
    return db.query(models.Meal).filter(models.Meal.user_id == user_id).all()