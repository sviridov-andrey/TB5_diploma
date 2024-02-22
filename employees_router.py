from typing import Annotated
from fastapi import APIRouter, Depends

from database import conn, connect_base
from schemas import EmployeeSchema


cur = connect_base()


router = APIRouter(
    prefix="/employees",
    tags=["Сотрудники"],
)


# Endpoint для создания сотрудника
@router.post("")
def create_employee(employee: Annotated[EmployeeSchema, Depends()]):
    """Добавить сотрудника"""
    cur.execute(
        "INSERT INTO employees (full_name, job_title, email) VALUES (%s, %s, %s) RETURNING id",
        (employee.full_name.title(), employee.job_title, employee.email)
    )
    employee_id = cur.fetchone()[0]
    conn.commit()
    return {"id": employee_id, **employee.dict()}
