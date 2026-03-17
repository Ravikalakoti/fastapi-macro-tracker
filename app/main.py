from fastapi import FastAPI

app = FastAPI(tilte="Macro and Nutrition Tracker API")

@app.get("/")
async def root():
	return {"message": "Welcome to Macro Tracker API"}