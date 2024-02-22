from typing import Annotated

from fastapi import APIRouter, Depends

from database import cur, conn
from schemas import EmployeeCreate, FieldID, EmployeeUpdate, TaskCreate, TaskUpdate

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


@router.put("/{task_id}")
def update_task(task: Annotated[TaskUpdate, Depends()]):
    """"Изменить данные задачи"""

    query_params = {}
    query_set = []

    if task.name is not None:
        query_params["name"] = task.name
        query_set.append("name = %s")

    if task.description is not None:
        query_params["description"] = task.description
        query_set.append("description = %s")

    if task.status is not None:
        query_params["status"] = task.status.value
        query_set.append("status = %s")

    if task.deadline is not None:
        query_params["deadline"] = task.deadline
        query_set.append("deadline = %s")

    if task.parent_task is not None:
        query_params["parent_task"] = task.parent_task
        query_set.append("parent_task = %s")

    if task.employee_id is not None:
        query_params["employee_id"] = task.employee_id
        query_set.append("employee_id = %s")

    values = list(query_params.values())
    values.append(task.id)

    query = "UPDATE tasks SET " + ", ".join(query_set) + " WHERE id = %s"

    cur.execute(query, values)
    conn.commit()

    return {"message": f"Внесены изменения {query_params}"}


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
