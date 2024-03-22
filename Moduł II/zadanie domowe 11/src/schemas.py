from datetime import date
from pydantic import BaseModel, Field, validator
from typing import Optional


class ContactIn(BaseModel):
    name: str = Field(max_length=25)
    lastname: str = Field(max_length=50)
    email: str = Field(max_length=100)
    phone: str = Field(max_length=15)
    birthday: date = None
    notes: str = Field(max_length=500)

    @validator('birthday', pre=True)
    def check_date_format(cls, birthday_date):
        if isinstance(birthday_date, str):
            if birthday_date == "":
                return None
            try:
                return date.fromisoformat(birthday_date)
            except ValueError:
                raise ValueError(
                    "Invalid date format. Required format: YYYY-MM-DD")
        return birthday_date


class ContactOut(ContactIn):
    id: int

    class Config:
        orm_mode = True


class ContactUpdate(BaseModel):
    name: Optional[str]
    lastname: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    birthday: Optional[date] = None
    notes: Optional[str]

    @validator('birthday', pre=True)
    def check_date_format(cls, birthday_date):
        if isinstance(birthday_date, str):
            if birthday_date == "":
                return None
            try:
                return date.fromisoformat(birthday_date)
            except ValueError:
                raise ValueError(
                    "Invalid date format. Required format: YYYY-MM-DD")
        return birthday_date


class ContactDelete(ContactIn):
    id: int

    class Config:
        orm_mode = True
