from fastapi import APIRouter


cars_router = APIRouter()


@cars_router.get("/cars")
def get_cars():
    return {"message": "Cars"}
