from datetime import datetime
from pydantic import BaseModel, EmailStr, parse_obj_as
from enum import Enum


class EmployeeCreate(BaseModel):
    full_name: str
    job_title: str
    email: EmailStr | None = None


class FieldID(BaseModel):
    id: int


class EmployeeUpdate(BaseModel):
    id: int
    full_name: str | None = None
    job_title: str | None = None
    email: EmailStr | None = None

class StatusList(Enum):
    important_task = "Важная задача"
    in_work = "В работе"
    completed = "Завершена"


class TaskCreate(BaseModel):
    name: str
    description: str
    status: StatusList
    deadline: datetime
    parent_task: int | None = None
    employee_id: int | None = None


