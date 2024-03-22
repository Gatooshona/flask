import pydantic
from typing import Optional, Type


class AbstractNotice(pydantic.BaseModel):
    title: str
    text: str
    owner_name: str

    @pydantic.field_validator('owner_name')
    @classmethod
    def check_owner_name(cls, v: str) -> str:
        if len(v) > 101:
            raise ValueError('Max is 100')
        return v


class CreateNotice(AbstractNotice):
    title: str
    text: str
    owner_name: str


class UpdateNotice(AbstractNotice):
    title: Optional[str]
    text: Optional[str]
    owner_name: Optional[str]


SCHEMA_CLASS = Type[CreateNotice | UpdateNotice]
SCHEMA = CreateNotice | UpdateNotice
