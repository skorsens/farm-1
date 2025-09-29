# ###############################################
# Requests
#

from typing import Annotated

from fastapi import FastAPI


app = FastAPI()


# ###############################################
# FastAPI processes routs in the order of their appearance.
# This route shall be before @app.get("/car/{id}"), otherwise
# the call "http get http://localhost:8000/car/my" fails, because "my" is not
# int
@app.get("/car/my")
def get_my_car():
    return {"car id": "my car"}


# ###############################################
# URL Path validation with type hints: any id value that is not int will fail:
# http get http://localhost:8000/car/1 - Good
# http get http://localhost:8000/car/billy - Bad
@app.get("/car/{id}")
def get_car(id: int):
    return {"car id": id}


# ###############################################
# URL Path validation with type hints and `Path`
# http get http://localhost:8000/account/free/3 - Good
# http get http://localhost:8000/account/freee/3 - Bad
# http get http://localhost:8000/account/free/1 - Bad
from enum import Enum
from fastapi import Path


class AccountType(Enum):
    FREE = "free"
    PRO = "pro"


@app.get("/account/{account_type}/{num_months}")
def get_account(account_type: AccountType, num_months: int = Path(..., ge=3, le=12)):
    return {"account_type": account_type, "num_months": num_months}


# ###############################################
# Query parameters
# http get "http://localhost:8000/cars/price?min_price=10&max_price=80"
# http get "http://localhost:8000/cars/price"
@app.get("/cars/price")
def get_cars_by_price(min_price: int = 0, max_price: int = 100):
    return {"message": f"min_price: {min_price}, max_price: {max_price}"}


# ###############################################
# Query parameters validation with the Query function
# http get "http://localhost:8000/cars/condition?min_condition=10&max_condition=80" - Good
# http get "http://localhost:8000/cars/condition?min_condition=10&max_condition=101" - Bad
# http get "http://localhost:8000/cars/condition?min_condition=10&max_condition=0" - Bad, but passes the validation
from fastapi import Query


@app.get("/cars/condition")
def get_cars_by_condition(
    min_condition: int = Query(0, ge=0, le=100),
    max_condition: int = Query(100, ge=0, le=100),
):
    return {
        "message": f"min_condition: {min_condition}, max_condition: {max_condition}"
    }


# ###############################################
# Request object
# http GET "http://localhost:8000/cars/request"
from fastapi import Request


@app.get("/cars/request")
def get_cars_request(request: Request):
    return {"message": f"{request.base_url=}, {dir(request)=}"}


# ###############################################
# Headers
from fastapi import Header


@app.get("/headers")
def get_headers(
    request: Request,
    non_existing_header_field: Annotated[str | None, Header()] = None,
    user_agent: Annotated[str | None, Header()] = None,
):
    return {
        "message": f"{user_agent=}, {non_existing_header_field=}, {request.headers=}"
    }


# ###############################################
# Cookies
# http GET "http://localhost:8000/cookies"
from fastapi import Cookie


@app.get("/cookies")
def get_cookies(request: Request):
    return {"message": f"{request.cookies=}"}


# ###############################################
# Response customization
# http GET http://localhost:8000/get_custom_response
from fastapi import status


@app.get("/get_custom_response", status_code=status.HTTP_208_ALREADY_REPORTED)
def get_custom_response():
    return {"message": "custom response"}
