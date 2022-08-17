from datetime import datetime, date

from pydantic import BaseModel, validator


class UserBase(BaseModel):
    first_name: str
    last_name: str
    password: str
    login: str
    birthday: date

    # @validator("birthdate", pre=True)
    # def parse_birthdate(cls, value):
    #     return datetime.strptime(
    #         value,
    #         "%d-%m-%Y"
    #     ).date()

