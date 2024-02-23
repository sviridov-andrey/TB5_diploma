from typing import Annotated

from fastapi import APIRouter, Depends

from database import connect
from schemas import EmployeeCreate, FieldID, EmployeeUpdate

router = APIRouter(
    prefix="/employees",
    tags=["Сотрудники"],
)


@router.post("")
def create_employee(employee: Annotated[EmployeeCreate, Depends()]):
    """Добавить сотрудника"""

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO employees (full_name, job_title, email) VALUES (%s, %s, %s) RETURNING id",
        (employee.full_name.title(), employee.job_title, employee.email)
    )
    employee_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return {"id": employee_id, **employee.dict()}


@router.get("/{employee_id}")
def read_employee(employee_id: Annotated[FieldID, Depends()]):
    """Получить сотрудника по id"""

    conn = connect()
    cur = conn.cursor()

    cur.execute(f"SELECT * FROM employees WHERE {employee_id}", employee_id)
    employee = cur.fetchone()
    if employee:
        employee_dict = {
            "id": employee[0],
            "full_name": employee[1],
            "job_title": employee[2],
            "email": employee[3],
        }
        cur.close()
        conn.close()
        return employee_dict
    else:
        cur.close()
        conn.close()
        return {"message": "Сотрудник не найден"}


@router.put("/{employee_id}")
def update_employee(employee: Annotated[EmployeeUpdate, Depends()]):
    """"Изменить данные сотрудника"""

    conn = connect()
    cur = conn.cursor()

    query_params = {}
    query_set = []

    if employee.full_name is not None:
        query_params["full_name"] = employee.full_name.title()
        query_set.append("full_name = %s")

    if employee.job_title is not None:
        query_params["job_title"] = employee.job_title
        query_set.append("job_title = %s")

    if employee.email is not None:
        query_params["email"] = employee.email
        query_set.append("email = %s")

    values = list(query_params.values())
    values.append(employee.id)

    query = "UPDATE employees SET " + ", ".join(query_set) + " WHERE id = %s"

    cur.execute(query, values)
    conn.commit()
    cur.close()
    conn.close()

    return {"message": f"Внесены изменения {query_params}"}


@router.delete("/{employee_id}")
def read_employee(employee_id: Annotated[FieldID, Depends()]):
    """Удалить сотрудника по id"""

    conn = connect()
    cur = conn.cursor()

    cur.execute(f"SELECT * FROM employees WHERE {employee_id}", employee_id)
    employee = cur.fetchone()

    if employee is None:

        cur.close()
        conn.close()
        return {"message": "Сотрудник с указанным ID не найден"}
    else:
        cur.execute(f"DELETE FROM employees WHERE {employee_id}", (employee_id,))
        conn.commit()
        cur.close()
        conn.close()

        return {"message": "Сотрудник удален"}
