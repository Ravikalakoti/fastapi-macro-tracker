from fastapi import FastAPI
from app.database import init_db
from app.apis import users, foods, meals

app = FastAPI(
    title="Macro Tracker API",
    description="Built by Ravi Singh Kalakoti \n\nA powerful API to track meals, calories, and macros.",
    version="1.0.0",
    contact={
        "name": "Ravi Singh Kalakoti",
        "email": "ravikalakoti16@gmail.com",
    }
)
init_db()


#Include Routers
app.include_router(users.router)
app.include_router(foods.router)
app.include_router(meals.router)

@app.get("/")
async def root():
	return {"message": "Welcome to Macro Tracker API"}