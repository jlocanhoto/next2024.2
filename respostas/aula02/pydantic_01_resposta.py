from dataclasses import dataclass
from datetime import date, datetime
from enum import Enum
from typing import Any, Optional, TypedDict

from pydantic import BaseModel


class Gender(str, Enum):
    MALE = 'masculino'
    FEMALE = 'feminino'
    NOT_INFORMED = 'prefiro nao informar'
    OTHER = 'outro'


class PersonalPreferences(TypedDict):
    topMovies: list[str]
    topFood: list[str]
    topMusic: list[str]


@dataclass
class Children:
    name: str
    birth_date: datetime | date


class Person(BaseModel):
    age: int
    salary: float
    name: str
    has_health_plan: bool
    address: str | None
    phone: Optional[str]
    nicknames: list[str]
    preferences: PersonalPreferences
    other_data: dict[str, Any]
    birth_date: datetime | date
    gender: Gender
    children: list[Children]
