from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from services.odoo import get_employee_by_pin, clock_in, clock_out
import os

router = APIRouter()

ALLOWED_IP = os.getenv("ALLOWED_IP")

class PINRequest(BaseModel):
    pin: str

class AttendanceRequest(BaseModel):
    pin: str

def verify_ip(request: Request):
    if not ALLOWED_IP:
        return
    forwarded_for = request.headers.get("x-forwarded-for")
    client_ip = forwarded_for.split(",")[0].strip() if forwarded_for else request.client.host
    if client_ip != ALLOWED_IP:
        raise HTTPException(status_code=403, detail=f"Access denied: {client_ip}")

@router.post("/attendance/checkin")
def checkin(data: AttendanceRequest, request: Request):
    verify_ip(request)
    employee = get_employee_by_pin(data.pin)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found or PIN incorrect")
    record_id = clock_in(employee['id'])
    return {"status": "clocked_in", "employee": employee['name'], "record_id": record_id}

@router.post("/attendance/checkout")
def checkout(data: AttendanceRequest, request: Request):
    verify_ip(request)
    employee = get_employee_by_pin(data.pin)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found or PIN incorrect")
    record_id = clock_out(employee['id'])
    if record_id is None:
        raise HTTPException(status_code=400, detail="No open clock-in found for this employee")
    return {"status": "clocked_out", "employee": employee['name'], "record_id": record_id}

@router.get("/employees")
def list_employees(request: Request):
    verify_ip(request)
    from services.odoo import list_all_employees
    result = list_all_employees()
    return {"employees": result}

@router.post("/attendance/status")
def attendance_status(data: AttendanceRequest, request: Request):
    verify_ip(request)
    employee = get_employee_by_pin(data.pin)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found or PIN incorrect")
    from services.odoo import get_attendance_status
    is_clocked_in = get_attendance_status(employee['id'])
    return {
        "employee": employee['name'],
        "employee_id": employee['id'],
        "is_clocked_in": is_clocked_in
    }
