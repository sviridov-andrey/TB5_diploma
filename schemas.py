from datetime import datetime
from pydantic import BaseModel, EmailStr
from enum import Enum
from typing import Optional


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
    important_task = "Создана"
    in_work = "В работе"
    completed = "Завершена"


class TaskUpdate(BaseModel):
    id: int
    name: str | None = None
    description: str | None = None
    status: StatusList
    deadline: datetime | None = None
    parent_task: Optional[int] = None
    employee_id: Optional[int] = None


class TaskCreate(BaseModel):
    name: str
    description: str
    status: StatusList
    deadline: datetime
    parent_task: int | None = None
    employee_id: int | None = None
