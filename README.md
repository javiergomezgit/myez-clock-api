# MyEZ Clock API

A FastAPI middleware service that connects to Odoo ERP via XML-RPC to manage employee clock-in/clock-out attendance records. Built for EZ Inflatables and deployed on Railway.

## Stack
- **FastAPI** — REST API layer
- **Odoo XML-RPC** — ERP integration for `hr.attendance` records
- **Railway** — PaaS deployment
- **IP Whitelisting** — office network restriction via `X-Forwarded-For`

## Endpoints
- `GET /employees` — returns all active employees
- `POST /attendance/status` — returns current clock status for employee by PIN
- `POST /attendance/checkin` — creates attendance record in Odoo
- `POST /attendance/checkout` — closes open attendance record in Odoo

## Live URL
`https://myez-clock-api-production.up.railway.app`

## iOS Client
Built with UIKit. Employees enter a PIN, app checks current status, and presents a single Clock In or Clock Out action that syncs directly to Odoo.
