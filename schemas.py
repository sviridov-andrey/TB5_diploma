from pydantic import BaseModel, EmailStr
from enum import Enum


class DegreeType(Enum):
    newbie = "newbie"
    expert = "expert"


class EmployeeCreate(BaseModel):
    full_name: str
    job_title: str
    email: EmailStr | None = None
  #  field: DegreeType


# Модель "Сотрудник"
class EmployeeID(BaseModel):
    id: int


class EmployeeUpdate(BaseModel):
    id: int
    full_name: str | None = None
    job_title: str | None = None
    email: EmailStr | None = None
