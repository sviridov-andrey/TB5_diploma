from pydantic import BaseModel, EmailStr
from enum import Enum


class DegreeType(Enum):
    newbie = "newbie"
    expert = "expert"


class EmployeeSchema(BaseModel):
    full_name: str
    job_title: str
    email: EmailStr | None
  #  field: DegreeType


# Модель "Сотрудник"
class Employee(EmployeeSchema):
    id: str
