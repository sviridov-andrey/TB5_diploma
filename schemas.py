from pydantic import BaseModel, EmailStr
from enum import Enum


class DegreeType(Enum):
    newbie = "newbie"
    expert = "expert"


class Employee(BaseModel):
    full_name: str
    job_title: str
    email: EmailStr | None = None
  #  field: DegreeType


# Модель "Сотрудник"
class EmployeeID(BaseModel):
    id: int
