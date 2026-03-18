from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud, models
from app.deps import get_db, get_current_user  # import the auth dependency
from datetime import date
from sqlalchemy import Date

router = APIRouter(prefix="/meals", tags=["meals"])

# Create a meal (only for logged-in user)
@router.post("/", response_model=schemas.MealOut)
def add_meal(
    meal: schemas.MealCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Create the meal instance
    db_meal = models.Meal(name=meal.name, user_id=current_user.id)

    # Fetch Food objects by IDs
    if meal.food_ids:
        db_meal.foods = db.query(models.Food).filter(models.Food.id.in_(meal.food_ids)).all()

    # Save to DB
    db.add(db_meal)
    db.commit()
    db.refresh(db_meal)
    return db_meal

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
    db_meal = db.query(models.Meal).filter(
        models.Meal.id == meal_id, 
        models.Meal.user_id == current_user.id
    ).first()
    
    if not db_meal:
        raise HTTPException(status_code=404, detail="Meal not found")

    # Update meal name
    db_meal.name = meal.name

    # Update foods if provided
    if meal.food_ids:
        db_meal.foods = db.query(models.Food).filter(models.Food.id.in_(meal.food_ids)).all()
    
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

@router.get("/summary/{summary_date}")
def daily_summary(summary_date: date, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    meals = db.query(models.Meal).filter(
        models.Meal.user_id == current_user.id,
        models.Meal.timestamp.cast(Date) == summary_date
    ).all()

    total_fat = sum(m.total_fat for m in meals)
    total_protein = sum(m.total_protein for m in meals)
    total_carbs = sum(m.total_carbs for m in meals)
    total_calories = total_fat*9 + (total_protein + total_carbs)*4

    return {
        "date": summary_date,
        "total_fat": total_fat,
        "total_protein": total_protein,
        "total_carbs": total_carbs,
        "total_calories": total_calories
    }