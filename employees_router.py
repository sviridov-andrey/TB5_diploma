from typing import Annotated
from fastapi import FastAPI, Depends

from database import cur, conn
from schemas import EmployeeSchema


# Endpoint для создания сотрудника
@app.post("/employees/")
def create_employee(employee: Annotated[EmployeeSchema, Depends()]):
    cur.execute(
        "INSERT INTO employees (full_name, job_title, email) VALUES (%s, %s, %s) RETURNING id",
        (employee.full_name.title(), employee.job_title, employee.email)
    )
    employee_id = cur.fetchone()[0]
    conn.commit()
    return {"id": employee_id, **employee.dict()}