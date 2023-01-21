from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class OperationKind(str, Enum):
    INCOME = 'income'
    OUTCOME = 'outcome'
    SALARY = 'salary'


class OperationBase(BaseModel):
    date: date
    kind: OperationKind
    amount: int
    description: Optional[str]


class Operation(OperationBase):  # Валидация типов  # один только id потому что остальное наследуем от Operation Base
    id: int

    class Config:
        orm_mode = True


class OperationCreate(OperationBase):
    pass   # Новых полей нет, поэтому пасс


class OperationUpdate(OperationBase):
    pass
