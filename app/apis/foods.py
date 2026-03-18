from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import schemas, crud, models
from app.deps import get_db, get_current_user

router = APIRouter(prefix="/foods", tags=["foods"])

# Add a new food (authenticated)
@router.post("/", response_model=schemas.FoodOut)
def add_food(
    food: schemas.FoodCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)  # require login
):
    return crud.create_food(db, food)

# List all foods (can be public or authenticated)
@router.get("/", response_model=list[schemas.FoodOut])
def get_foods(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)  # optional, remove if public
):
    return crud.list_foods(db)

#update food
@router.put("/{food_id}", response_model=schemas.FoodOut)
def update_food(
    food_id: int,
    food: schemas.FoodCreate,  # use a separate schema if you want PATCH
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    db_food = db.query(models.Food).filter(models.Food.id == food_id).first()
    if not db_food:
        raise HTTPException(status_code=404, detail="Food not found")
    for key, value in food.dict().items():
        setattr(db_food, key, value)
    db.commit()
    db.refresh(db_food)
    return db_food

# Delete food
@router.delete("/{food_id}", status_code=204)
def delete_food(
    food_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    db_food = db.query(models.Food).filter(models.Food.id == food_id).first()
    if not db_food:
        raise HTTPException(status_code=404, detail="Food not found")
    db.delete(db_food)
    db.commit()
    return None  # 204 No Content