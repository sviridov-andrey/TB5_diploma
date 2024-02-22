from typing import Annotated

from fastapi import APIRouter, Depends

from database import cur, conn
from schemas import EmployeeCreate, FieldID, EmployeeUpdate, TaskCreate

router = APIRouter(
    prefix="/tasks",
    tags=["Задачи"],
)


@router.post("")
def create_task(task: Annotated[TaskCreate, Depends()]):
    """Добавить задачу"""

    cur.execute(
        f"INSERT INTO tasks (name, description, status, deadline, parent_task, employee_id) "
        f"VALUES (%s, %s, %s, %s, %s, %s) RETURNING id",
        (task.name, task.description, task.status.value, task.deadline, task.parent_task, task.employee_id)
    )
    task_id = cur.fetchone()[0]
    conn.commit()
    return {"id": task_id, **task.dict()}


@router.get("/{task_id}")
def read_task(task_id: Annotated[FieldID, Depends()]):
    """Получить задачу по id"""

    cur.execute(f"SELECT * FROM tasks WHERE {task_id}", task_id)
    task = cur.fetchone()
    print(task)
    if task:
        task_dict = {
            "id": task[0],
            "name": task[1],
            "description": task[2],
            "status": task[3],
            "deadline": task[4],
            "parent_task": task[5],
            "employee_id": task[6],
        }
        return task_dict
    else:
        return {"message": "Задача не найдена"}
#
#
# @router.put("/{task_id}")
# def update_task(task: Annotated[EmployeeUpdate, Depends()]):
#     """"Изменить данные сотрудника"""
#
#     query_params = {}
#     query_set = []
#
#     if task.full_name is not None:
#         query_params["full_name"] = task.full_name
#         query_set.append("full_name = %s")
#
#     if task.job_title is not None:
#         query_params["job_title"] = task.job_title
#         query_set.append("job_title = %s")
#
#     if task.email is not None:
#         query_params["email"] = task.email
#         query_set.append("email = %s")
#
#     values = list(query_params.values())
#     values.append(task.id)
#
#     query = "UPDATE tasks SET " + ", ".join(query_set) + " WHERE id = %s"
#
#     cur.execute(query, values)
#     conn.commit()
#
#     return {"message": f"Внесены изменения {query_params}"}
#
#
# @router.delete("/{task_id}")
# def read_task(task_id: Annotated[EmployeeID, Depends()]):
#     """Удалить сотрудника по id"""
#
#     cur.execute(f"SELECT * FROM tasks WHERE {task_id}", task_id)
#     task = cur.fetchone()
#
#     if task is None:
#
#         return {"message": "Сотрудник с указанным ID не найден"}
#     else:
#         cur.execute(f"DELETE FROM tasks WHERE {task_id}", (task_id,))
#         conn.commit()
#
#         return {"message": "Сотрудник удален"}
