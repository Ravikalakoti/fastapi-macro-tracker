from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app import crud, schemas
from app.deps import get_db, get_current_user
from app.auth import create_access_token
from app.models import User

router = APIRouter(prefix="/users", tags=["users"])

# Register stays the same
@router.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already exists!")
    return crud.create_user(db, user)

# Login using OAuth2 form
@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, form_data.username)
    if not db_user or not crud.verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token({"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=schemas.UserOut)
def read_current_user(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return current_user

@router.put("/me", response_model=schemas.UserOut)
def update_user(
    user_update: schemas.UserUpdate,  # create this schema with fields like full_name, email, password
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # If user wants to update password, hash it
    if user_update.password:
        user_update.password = crud.pwd_context.hash(user_update.password)
    return crud.update_user(db, current_user.id, user_update)

@router.delete("/me", status_code=204)
def delete_user(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    crud.delete_user(db, current_user.id)
    return {"detail": "Account deleted successfully"}