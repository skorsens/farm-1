from fastapi import FastAPI
from try_fastapi_APIRouter_cars import cars_router
from try_fastapi_APIRouter_users import users_router

# http GET http://127.0.0.1:8000/cars-prefix/cars
# http GET http://127.0.0.1:8000/users-prefix/users
app = FastAPI()

app.include_router(cars_router, prefix="/cars-prefix", tags=["cars-tags"])
app.include_router(users_router, prefix="/users-prefix", tags=["users-tags"])
