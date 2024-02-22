from fastapi import FastAPI, Depends
import uvicorn
from create_tables import CreateTables
from database import cur, conn
from employees_router import router as employees_router
from typing import Annotated

from schemas import EmployeeCreate

create_tables = CreateTables()
create_tables.create_tables()

app = FastAPI()
app.include_router(employees_router)

# @app.post("/")
# def create_employee(employee: Annotated[Employee, Depends()]):
#
#     cur.execute(
#         "INSERT INTO employees (full_name, job_title, email) VALUES (%s, %s, %s) RETURNING id",
#         (employee.full_name.title(), employee.job_title, employee.email)
#     )
#     employee_id = cur.fetchone()[0]
#     conn.commit()
#     return {"id": employee_id, **employee.dict()}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
