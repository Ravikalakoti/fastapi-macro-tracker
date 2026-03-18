from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app import crud, schemas
from app.deps import get_db, get_current_user
from app.auth import create_access_token
from app.models import User
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import os
from dotenv import load_dotenv

load_dotenv()

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
APP_HOST = os.getenv("APP_HOST", "http://localhost:8000")

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register", response_model=schemas.UserOut)
async def register(user: schemas.UserCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already exists!")

    new_user = crud.create_user(db, user)
    background_tasks.add_task(send_registration_emails, new_user)
    return new_user

async def send_registration_emails(user: User):
    """Send Ravi Kalakoti branded HTML emails - FIXED"""

    # 1. WELCOME EMAIL (Ravi Kalakoti Branded)
    welcome_msg = MIMEMultipart("alternative")
    welcome_msg['Subject'] = f"Welcome to Macro Tracker, {user.username}! 👋"
    welcome_msg['From'] = SENDER_EMAIL
    welcome_msg['To'] = user.email
    
    html_welcome = f"""
    <!DOCTYPE html>
    <html>
    <head><meta charset="UTF-8"></head>
    <body style="margin:0;padding:0;font-family:'Segoe UI',sans-serif;background:#f4f4f4">
        <table role="presentation" width="100%" style="max-width:600px;margin:20px auto">
            <tr>
                <td style="background:linear-gradient(135deg,#2c3e50,#3498db);padding:30px;text-align:center;border-radius:15px 15px 0 0">
                    <h1 style="color:white;margin:0;font-size:28px">🎯 Macro Tracker</h1>
                    <p style="color:#ecf0f1;margin:5px 0 0 0;font-size:16px">
                        by <strong>Ravi Kalakoti</strong> | Backend Developer
                    </p>
                </td>
            </tr>
            <tr>
                <td style="background:white;padding:40px;border-radius:0 0 15px 15px;box-shadow:0 10px 30px rgba(0,0,0,0.1)">
                    <h2 style="color:#2c3e50;text-align:center">Welcome aboard, {user.full_name or user.username}! 🚀</h2>
                    <p style="font-size:16px;line-height:1.6;color:#555;text-align:center">
                        Your account is ready! Start tracking your macros and achieve your fitness goals.
                    </p>
                    <div style="text-align:center;margin:30px 0">
                        <a href="http://localhost:8000/docs" style="background:#3498db;color:white;padding:15px 40px;text-decoration:none;border-radius:50px;font-weight:bold;font-size:16px;display:inline-block">Start Tracking Now</a>
                    </div>
                    <table style="width:100%;margin:30px 0">
                        <tr><td style="padding:15px;background:#f8f9fa;border-radius:10px"><strong>👤 Username:</strong> {user.username}</td></tr>
                        <tr><td style="padding:15px;background:#f8f9fa;border-radius:10px"><strong>📧 Email:</strong> {user.email}</td></tr>
                    </table>
                </td>
            </tr>
            <tr>
                <td style="background:#34495e;color:white;padding:25px;text-align:center;border-radius:15px;font-size:14px">
                    <p>Built with ❤️ by <a href="https://www.linkedin.com/in/ravi-kalakoti/" style="color:#3498db">Ravi Kalakoti</a></p>
                    <p>Python | Django | FastAPI | Backend Developer | Bageshwar, Uttarakhand</p>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """
    
    # ✅ FIXED: Use MIMEText instead of non-existent MIMEHTMLPart
    html_part = MIMEText(html_welcome, 'html')
    welcome_msg.attach(html_part)
    
    # 2. ADMIN NOTIFICATION
    admin_msg = MIMEMultipart("alternative")
    admin_msg['Subject'] = "📊 New User Registered - Ravi Kalakoti Dashboard"
    admin_msg['From'] = SENDER_EMAIL
    admin_msg['To'] = ADMIN_EMAIL
    
    html_admin = f"""
    <!DOCTYPE html>
    <html>
    <head><meta charset="UTF-8"></head>
    <body style="margin:0;padding:0;font-family:'Segoe UI',monospace;background:#1a1a1a">
        <table role="presentation" width="100%" style="max-width:600px;margin:20px auto">
            <tr>
                <td style="background:linear-gradient(135deg,#667eea,#764ba2);padding:25px;text-align:center;color:white;border-radius:15px">
                    <h1 style="margin:0;font-size:24px">👨‍💻 Ravi Kalakoti Dashboard</h1>
                    <p style="margin:5px 0 0 0">Macro Tracker - New Registration Alert</p>
                </td>
            </tr>
            <tr>
                <td style="background:#2c3e50;padding:30px;border-radius:15px;color:white">
                    <div style="background:white;color:#2c3e50;padding:25px;border-radius:10px;margin-bottom:20px">
                        <h3 style="margin:0 0 20px 0;color:#2c3e50;text-align:center">New User Joined! 🎉</h3>
                        <table style="width:100%;font-size:16px">
                            <tr><td style="padding:12px 0;font-weight:bold">🆔 Username:</td><td style="padding:12px 0">{user.username}</td></tr>
                            <tr><td style="padding:12px 0;font-weight:bold">📧 Email:</td><td style="padding:12px 0">{user.email}</td></tr>
                            <tr><td style="padding:12px 0;font-weight:bold">👤 Name:</td><td style="padding:12px 0">{user.full_name or 'N/A'}</td></tr>
                        </table>
                    </div>
                </td>
            </tr>
            <tr>
                <td style="background:#34495e;padding:20px;text-align:center;border-radius:15px;color:#bdc3c7;font-size:13px">
                    <p>Developed by <a href="https://www.linkedin.com/in/ravi-kalakoti/" style="color:#3498db">Ravi Kalakoti</a></p>
                    <p>📍 Bageshwar, Uttarakhand | 💻 Python/Django/FastAPI Developer</p>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """
    
    # ✅ FIXED: Use MIMEText instead of non-existent MIMEHTMLPart
    html_part_admin = MIMEText(html_admin, 'html')
    admin_msg.attach(html_part_admin)
    
    # Send emails
    await aiosmtplib.send(welcome_msg, hostname="smtp.gmail.com", port=465, username=SENDER_EMAIL, password=SENDER_PASSWORD, use_tls=True)
    await aiosmtplib.send(admin_msg, hostname="smtp.gmail.com", port=465, username=SENDER_EMAIL, password=SENDER_PASSWORD, use_tls=True)


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
