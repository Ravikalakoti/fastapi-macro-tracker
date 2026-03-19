from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import init_db
from app.apis import users, foods, meals

app = FastAPI(
    title="Macro Tracker API",
    description=(
        "**Built by Ravi Singh Kalakoti**\n\n"
        "A powerful API to track meals, calories, and macros.\n\n"
        "***Connect with me***:\n"
        "- [LinkedIn](https://www.linkedin.com/in/ravi-kalakoti/)\n"
        "- [GitHub](https://github.com/Ravikalakoti)\n"
        "- [HackerRank](https://www.hackerrank.com/profile/ravikalakoti)"
    ),
    version="1.0.0",
    contact={
        "name": "Ravi Singh Kalakoti",
        "email": "ravikalakoti16@gmail.com",
        "url": "https://www.linkedin.com/in/ravi-kalakoti/"
    }
)
init_db()

# Allow requests from your frontend
origins = [
    "http://localhost:5173",  # React dev server
	"https://macro-tracker-frontend.onrender.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Include Routers
app.include_router(users.router)
app.include_router(foods.router)
app.include_router(meals.router)

@app.get("/health")
async def root():
	return {"message": "Welcome to Macro Tracker API"}
