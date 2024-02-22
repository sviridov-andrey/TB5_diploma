from typing import Annotated
from urllib import response

from fastapi import APIRouter, Depends

from database import cur, conn
from schemas import Employee, EmployeeID


router = APIRouter(
    prefix="/employees",
    tags=["Сотрудники"],
)


@router.post("")
def create_employee(employee: Annotated[Employee, Depends()]):
    """Добавить сотрудника"""

    cur.execute(
        "INSERT INTO employees (full_name, job_title, email) VALUES (%s, %s, %s) RETURNING id",
        (employee.full_name.title(), employee.job_title, employee.email)
    )
    employee_id = cur.fetchone()[0]
    conn.commit()
    return {"id": employee_id, **employee.dict()}


@router.get("/{employee_id}")
def read_employee(employee_id: Annotated[EmployeeID, Depends()]):
    """Получить сотрудника по id"""

    cur.execute(f"SELECT * FROM employees WHERE {employee_id}", employee_id)
    employee = cur.fetchone()
    if employee:
        employee_dict = {
            "id": employee[0],
            "full_name": employee[1],
            "job_title": employee[2],
            "email": employee[3],
        }
        return employee_dict
    else:
        return {"message": "Сотрудник не найден"}
