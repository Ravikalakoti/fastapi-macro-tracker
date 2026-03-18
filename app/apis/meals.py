from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud, models
from app.deps import get_db, get_current_user  # import the auth dependency

router = APIRouter(prefix="/meals", tags=["meals"])

# Create a meal (only for logged-in user)
@router.post("/", response_model=schemas.MealOut)
def add_meal(
    meal: schemas.MealCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    meal.user_id = current_user.id
    return crud.create_meal(db, meal)

# Get meals of the current logged-in user
@router.get("/", response_model=list[schemas.MealOut])
def get_my_meals(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return crud.list_user_meals(db, current_user.id)

# ------------------ Update Meal ------------------
@router.put("/{meal_id}", response_model=schemas.MealOut)
def update_meal(
    meal_id: int,
    meal: schemas.MealCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    db_meal = db.query(models.Meal).filter(models.Meal.id == meal_id, models.Meal.user_id == current_user.id).first()
    if not db_meal:
        raise HTTPException(status_code=404, detail="Meal not found")
    # Update all fields
    for key, value in meal.dict().items():
        setattr(db_meal, key, value)
    db.commit()
    db.refresh(db_meal)
    return db_meal

# ------------------ Delete Meal ------------------
@router.delete("/{meal_id}", status_code=204)
def delete_meal(
    meal_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    db_meal = db.query(models.Meal).filter(models.Meal.id == meal_id, models.Meal.user_id == current_user.id).first()
    if not db_meal:
        raise HTTPException(status_code=404, detail="Meal not found")
    db.delete(db_meal)
    db.commit()
    return None  # 204 No Content
