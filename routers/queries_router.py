from typing import Annotated
from fastapi import APIRouter, Depends
from database import connect
from schemas import EmployeeCreate, FieldID, EmployeeUpdate


router = APIRouter(
    prefix="/queries",
    tags=["Запросы к базе данных"],
)


@router.get("/busy_employees")
def busy_employees():
    """Запрашивает из БД список сотрудников и их задачи, отсортированный по количеству активных задач"""

    conn = connect()
    cur = conn.cursor()

    query = """
    SELECT e.full_name, e.job_title, COUNT(t.employee_id) AS количество_активных_задач
    FROM employees e
    LEFT JOIN tasks t ON e.id = t.employee_id AND t.status = 'В работе'
    WHERE t.employee_id IS NOT NULL
    GROUP BY e.full_name, e.job_title
    ORDER BY количество_активных_задач;
    """

    cur.execute(query)
    result = [dict(zip([column[0] for column in cur.description], row)) for row in cur.fetchall()]

    return result
