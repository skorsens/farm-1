from fastapi import FastAPI

app = FastAPI()

from pydantic import BaseModel
from fastapi import Body


# ###############################################
# Function parameters
#
# The function parameters will be recognized as follows:
#
# If the parameter is also declared in the path, it will be used as a path parameter.
# If the parameter is of a singular type (like int, float, str, bool, etc) it will be interpreted as a query parameter.
# If the parameter is declared to be of the type of a Pydantic model, it will be interpreted as a request body.


# ###############################################
# Post dict body
# http POST "http://localhost:8000/post_dict_body" brand="FIAT" model="500" year=2015


@app.post("/post_dict_body")
def post_dict_body(data: dict = Body(...)):
    return {"message": f"{data=}"}


# ###############################################
# Use pydantic.BaseModel
# http POST "http://127.0.0.1:8000/post_data1" sField="sField" nField=1
#


class Data1(BaseModel):
    sField: str
    nField: int


@app.post("/post_data1")
def post_data1(mydata: Data1):
    return {"message": f"{mydata=}"}


class Data2(BaseModel):
    sField: str
    nField: int


@app.post("/post_data1_data2")
def post_data1_data2(data1: Data1, data2: Data2):
    return {"message": f"{data1=}, {data2=}"}


@app.post("/post_data2_data1_param")
def post_data1_data2_param(data2: Data2, data1: Data1, param: int = Body(...)):
    return {"message": f"{data2=}, {data1=}, {param=}"}


# ###############################################
# HTTP Error Status code
# http POST http://localhost:8000/post_status_code str_field="str1" status_code=1
#
from fastapi import HTTPException, status


class DataForStatusCode(BaseModel):
    str_field: str
    status_code: int


@app.post("/post_status_code")
def post_status_code(data: DataForStatusCode):
    raise HTTPException(
        status_code=status.HTTP_406_NOT_ACCEPTABLE,
        detail=f"Returning {data.status_code=}",
    )


# ###############################################
# Forms
# http -f POST localhost:8000/upload  brand='Ferrari' model='Testarossa'  file@fastapi_hello_world.py
import shutil
from fastapi import Request, Form, File, UploadFile


@app.post("/upload")
def upload_file(
    request: Request,
    file: UploadFile = File(...),
    brand: str = Form(...),
    model: str = Form(...),
):
    with open("saved_fastapi_hello_world.py", "wb") as saved_file:
        shutil.copyfileobj(file.file, saved_file)

    return {
        "filename": file.filename,
        "brand": brand,
        "model": model,
        "request.form": request.form,
    }
