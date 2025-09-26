from datetime import datetime
from typing import Literal

from pydantic import (
    BaseModel,
    ValidationError,
    StrictInt,
    Field,
    EmailStr,
    ConfigDict,
    field_serializer,
)


class User(BaseModel):
    id: StrictInt
    username: str
    email: str
    dob: datetime
    account: Literal["personal", "business"] = "personal"
    nickname: str | None = None


good_user = User(
    id=1, username="freethrow", email="email@gmail.com", dob=datetime(1975, 5, 13)
)

try:
    bad_user = User(
        id="one",
        username="freethrow",
        email="email@gmail.com",
        dob=datetime(1975, 5, 13),
    )
except BaseException as ex:
    assert type(ex) is ValidationError
    assert (
        str(ex)
        == """1 validation error for User
id
  Input should be a valid integer [type=int_type, input_value='one', input_type=str]
    For further information visit https://errors.pydantic.dev/2.11/v/int_type"""
    ), f'Shall be: "{str(ex)}"'

assert (
    str(good_user)
    == "id=1 username='freethrow' email='email@gmail.com' dob=datetime.datetime(1975, 5, 13, 0, 0) account='personal' nickname=None"
), f'Shall be: "{str(good_user)}"'

# No validation for specific fields
good_user.id = "one"

deserialized_user = User.model_validate(
    {
        "id": 3,
        "username": "username3",
        "email": "username3@email.com",
        "dob": datetime(1975, 5, 13),
    }
)


class UserWithFields(BaseModel):
    id: StrictInt = Field()
    username: str = Field(min_length=5, max_length=50)
    email: EmailStr = Field()
    dob: datetime = Field(...)
    account: Literal["personal", "business"] = Field(default="personal")
    nickname: str | None = Field(default=None)
    password: str = Field(min_length=5, max_length=20, pattern="^[a-zA-Z0-9]+$")


userWithFieldsGood = UserWithFields(
    id=1,
    username="freethrow",
    email="freethrow@email.com",
    dob=datetime(1975, 5, 13),
    password="password123",
)


try:
    userWithFieldsBad = UserWithFields(
        id=1,
        username="freethrow",
        email="freethrow",
        dob=datetime(1975, 5, 13),
        password="password123",
    )
except BaseException as ex:
    assert type(ex) is ValidationError
    assert (
        str(ex)
        == """1 validation error for UserWithFields
email
  value is not a valid email address: An email address must have an @-sign. [type=value_error, input_value='freethrow', input_type=str]"""
    ), f'Shall be: "{str(ex)}"'


assert userWithFieldsGood.model_dump() == {
    "id": 1,
    "username": "freethrow",
    "email": "freethrow@email.com",
    "dob": datetime(1975, 5, 13, 0, 0),
    "account": "personal",
    "nickname": None,
    "password": "password123",
}
assert (
    userWithFieldsGood.model_dump_json()
    == '{"id":1,"username":"freethrow","email":"freethrow@email.com","dob":"1975-05-13T00:00:00","account":"personal","nickname":null,"password":"password123"}'
)
assert (
    userWithFieldsGood.model_dump_json(exclude={"password", "dob", "account"})
    == '{"id":1,"username":"freethrow","email":"freethrow@email.com","nickname":null}'
)

assert userWithFieldsGood.model_json_schema() == {
    "properties": {
        "id": {"title": "Id", "type": "integer"},
        "username": {
            "maxLength": 50,
            "minLength": 5,
            "title": "Username",
            "type": "string",
        },
        "email": {"format": "email", "title": "Email", "type": "string"},
        "dob": {"format": "date-time", "title": "Dob", "type": "string"},
        "account": {
            "default": "personal",
            "enum": ["personal", "business"],
            "title": "Account",
            "type": "string",
        },
        "nickname": {
            "anyOf": [{"type": "string"}, {"type": "null"}],
            "default": None,
            "title": "Nickname",
        },
        "password": {
            "maxLength": 20,
            "minLength": 5,
            "pattern": "^[a-zA-Z0-9]+$",
            "title": "Password",
            "type": "string",
        },
    },
    "required": ["id", "username", "email", "dob", "password"],
    "title": "UserWithFields",
    "type": "object",
}


# ConfigDict
class UserModelWithConfigDict(BaseModel):
    id: int = Field()
    username: str = Field(min_length=5, max_length=20, alias="name")
    password: str = Field(min_length=5, max_length=20, pattern="^[a-zA-Z0-9]+$")
    model_config = ConfigDict(extra="forbid", populate_by_name=True)


userModelWithConfigDictGood = UserModelWithConfigDict(
    id=1,
    username="freethrow",
    password="password123",
)

try:
    userModelWithConfigDictBad = UserModelWithConfigDict(
        id=1,
        username="freethrow",
        email="freethrow@email.com",
        password="password123",
    )
except BaseException as ex:
    assert type(ex) is ValidationError
    assert (
        str(ex)
        == """1 validation error for UserModelWithConfigDict
email
  Extra inputs are not permitted [type=extra_forbidden, input_value='freethrow@email.com', input_type=str]
    For further information visit https://errors.pydantic.dev/2.11/v/extra_forbidden"""
    )


# field_serializer
class Account(BaseModel):
    balance: float
    updated: datetime

    @field_serializer("balance", when_used="always")
    def serialize_balance(self, value: float) -> float:
        return round(value, 2)

    @field_serializer("updated", when_used="json")
    def serialize_updated(self, value: datetime) -> str:
        return value.isoformat()


updated = datetime.now()
account_data = {
    "balance": 123.45545,
    "updated": updated,
}
account = Account.model_validate(account_data)
assert account.model_dump() == {
    "balance": 123.46,
    "updated": updated,
}
assert (
    account.model_dump_json()
    == f'{{"balance":123.46,"updated":"{updated.isoformat()}"}}'
)


# field_validator
from pydantic import field_validator


class Article(BaseModel):
    id: int = Field()
    title: str
    content: str

    @field_validator("title")
    @classmethod
    def validate_title(cls, title: str) -> str:
        if "FARM stack" not in title:
            raise ValueError(f"FARM stack is not in title {title}")
        return title


articleGoodData = {
    "id": 1,
    "title": "Title with FARM stack in it",
    "content": "FARM stack",
}
articleGoog = Article.model_validate(articleGoodData)
assert articleGoog.model_dump() == {
    "id": 1,
    "title": "Title with FARM stack in it",
    "content": "FARM stack",
}


articleBadData = {"id": 1, "title": "Title", "content": "FARM stack"}

try:
    articleBad = Article.model_validate(articleBadData)
except BaseException as ex:
    assert type(ex) is ValidationError
    assert (
        str(ex)
        == """1 validation error for Article
title
  Value error, FARM stack is not in title Title [type=value_error, input_value='Title', input_type=str]
    For further information visit https://errors.pydantic.dev/2.11/v/value_error"""
    )

# model_validator
from pydantic import model_validator
from typing import Any, Self


class UserModelV(BaseModel):
    id: int
    username: str
    email: EmailStr
    password1: str
    password2: str

    @model_validator(mode="before")
    @classmethod
    def validate_private_data(cls, data: Any) -> Any:
        if isinstance(data, dict):
            assert "private_data" not in data, "private_data shall not be in the data"
        return data

    @model_validator(mode="after")
    def validate_passwords_match(self) -> Self:
        if self.password1 != self.password2:
            raise ValueError("passwords do not match")

        return self


usr_data1 = {
    "id": 1,
    "username": "freethrow",
    "email": "email@gmail.com",
    "password1": "password123",
    "password2": "password123",
    "private_data": "some private data",
}

usr_data2 = {
    "id": 1,
    "username": "freethrow",
    "email": "email@gmail.com",
    "password1": "password123",
    "password2": "password456",
}

try:
    userModelV1 = UserModelV.model_validate(usr_data1)
except BaseException as ex:
    assert type(ex) is ValidationError
    assert (
        str(ex)
        == """1 validation error for UserModelV
  Assertion failed, private_data shall not be in the data [type=assertion_error, input_value={'id': 1, 'username': 'fr...a': 'some private data'}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.11/v/assertion_error"""
    )

try:
    userModelV2 = UserModelV.model_validate(usr_data2)
except BaseException as ex:
    assert type(ex) is ValidationError
    assert (
        str(ex)
        == """1 validation error for UserModelV
  Value error, passwords do not match [type=value_error, input_value={'id': 1, 'username': 'fr...ssword2': 'password456'}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.11/v/value_error"""
    )


# Nested models


class CarModel(BaseModel):
    model: str
    year: int


class CarBrand(BaseModel):
    brand: str
    models: list[CarModel]
    country: str


ford_car_brand_data = {
    "brand": "Ford",
    "models": [
        {"model": "Mustang", "year": 1964},
        {"model": "Focus", "year": 1975},
        {"model": "Explorer", "year": 1999},
    ],
    "country": "USA",
}

fordCarBrand = CarBrand.model_validate(ford_car_brand_data)

# pydantic-settings
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_url: str = Field(default="")
    secret_key: str = Field(default="")

    class Config:
        env_file = ".env"


settings1FromEnvFile = Settings()
assert settings1FromEnvFile.model_dump() == {
    "api_url": "https://api.com/v2",
    "secret_key": "s3cretstr1n6",
}

# os.environ has precedence over .env config file
import os

try:
    os.environ["secret_key"] = "secret-from-os.environ"
    settings1FromEnvFileAndOsEnviron = Settings()

    assert settings1FromEnvFileAndOsEnviron.model_dump() == {
        "api_url": "https://api.com/v2",
        "secret_key": "secret-from-os.environ",
    }
finally:
    del os.environ["secret_key"]
