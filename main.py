from fastapi import FastAPI
from routers.attendance import router as attendance_router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="EZClock API")

app.include_router(attendance_router)

@app.get("/")
def root():
    return {"status": "EZClock API running"}
