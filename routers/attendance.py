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
    client_ip = request.client.host
    if ALLOWED_IP and client_ip != ALLOWED_IP:
        raise HTTPException(status_code=403, detail="Access denied: unauthorized network")

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
