from fastapi import FastAPI
from app.database import init_db

app = FastAPI(tilte="Macro and Nutrition Tracker API")
init_db()

@app.get("/")
async def root():
	return {"message": "Welcome to Macro Tracker API"}