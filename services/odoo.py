import xmlrpc.client
import os
from dotenv import load_dotenv

load_dotenv()

def get_config():
    return {
        "url": os.getenv("ODOO_URL"),
        "db": os.getenv("ODOO_DB"),
        "username": os.getenv("ODOO_USERNAME"),
        "api_key": os.getenv("ODOO_API_KEY"),
    }

def get_uid(cfg):
    common = xmlrpc.client.ServerProxy(f"{cfg['url']}/xmlrpc/2/common")
    return common.authenticate(cfg['db'], cfg['username'], cfg['api_key'], {})

def get_models(cfg):
    return xmlrpc.client.ServerProxy(f"{cfg['url']}/xmlrpc/2/object")

def get_employee_by_pin(pin: str):
    cfg = get_config()
    uid = get_uid(cfg)
    models = get_models(cfg)
    result = models.execute_kw(cfg['db'], uid, cfg['api_key'],
        'hr.employee', 'search_read',
        [[['pin', '=', pin], ['active', '=', True]]],
        {'fields': ['id', 'name', 'pin'], 'limit': 1}
    )
    return result[0] if result else None

def clock_in(employee_id: int):
    from datetime import datetime, timezone
    cfg = get_config()
    uid = get_uid(cfg)
    models = get_models(cfg)
    now = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    record_id = models.execute_kw(cfg['db'], uid, cfg['api_key'],
        'hr.attendance', 'create',
        [{'employee_id': employee_id, 'check_in': now}]
    )
    return record_id

def clock_out(employee_id: int):
    from datetime import datetime, timezone
    cfg = get_config()
    uid = get_uid(cfg)
    models = get_models(cfg)
    now = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    open_records = models.execute_kw(cfg['db'], uid, cfg['api_key'],
        'hr.attendance', 'search_read',
        [[['employee_id', '=', employee_id], ['check_out', '=', False]]],
        {'fields': ['id'], 'limit': 1}
    )
    if not open_records:
        return None
    record_id = open_records[0]['id']
    models.execute_kw(cfg['db'], uid, cfg['api_key'],
        'hr.attendance', 'write',
        [[record_id], {'check_out': now}]
    )
    return record_id

def list_all_employees():
    cfg = get_config()
    uid = get_uid(cfg)
    models = get_models(cfg)
    return models.execute_kw(cfg['db'], uid, cfg['api_key'],
        'hr.employee', 'search_read',
        [[['active', '=', True]]],
        {'fields': ['id', 'name'], 'limit': 100}
    )
