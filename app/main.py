from fastapi import FastAPI
from app.database import init_db
from app.apis import users

app = FastAPI(tilte="Macro and Nutrition Tracker API")
init_db()


#Include Routers
app.include_router(users.router)

@app.get("/")
async def root():
	return {"message": "Welcome to Macro Tracker API"}