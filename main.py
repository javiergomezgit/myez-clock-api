from fastapi import FastAPI
from routers.attendance import router as attendance_router
from dotenv import load_dotenv
from fastapi import FastAPI, Request

load_dotenv()

app = FastAPI(title="EZClock API")

app.include_router(attendance_router)

@app.get("/")
def root(request: Request):
    forwarded_for = request.headers.get("x-forwarded-for")
    client_ip = forwarded_for.split(",")[0].strip() if forwarded_for else request.client.host
    return {"status": "EZClock API running", "your_ip": client_ip}
