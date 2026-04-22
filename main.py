from fastapi import FastAPI
from routers.attendance import router as attendance_router
from dotenv import load_dotenv
from fastapi import FastAPI, Request

load_dotenv()

app = FastAPI(title="EZClock API")

app.include_router(attendance_router)

@app.get("/")
def root(request: Request):
    return {"status": "EZClock API running", "your_ip": request.client.host}
