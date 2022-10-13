from typing import Any
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import as_declarative, declared_attr
import sqlalchemy.sql.functions as F
from typing import cast
import re

pattern_camel_case = r"(?<!^)(?=[A-Z])"


def camel_case_to_snake_case(string: str):
    return re.sub(pattern_camel_case, "_", string).lower()


@as_declarative()
class Base:
    id: Any
    __name__: str
    # Generate __tablename__ automatically

    @declared_attr
    def __tablename__(cls) -> str:
        return camel_case_to_snake_case(cls.__name__)


class IdMixIn(object):
    id = cast(int, Column(Integer, primary_key=True, index=True, autoincrement=True))


class CreateTimeMixIn(object):
    created_time = Column(DateTime(timezone=True), server_default=F.now())
    modified_time = Column(DateTime(timezone=True), server_onupdate=F.now())


class IdWithCreateTimeMixIn(CreateTimeMixIn, IdMixIn):
    ...


class NameWithCreateTimeMixIn(IdWithCreateTimeMixIn):
    name = cast(str, Column(String, nullable=False, unique=False))
