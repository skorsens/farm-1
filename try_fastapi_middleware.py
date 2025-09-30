from fastapi import FastAPI, Request


app = FastAPI()

# http GET http://127.0.0.1:8000/


@app.middleware("http")
async def add_int_header(request: Request, call_next):
    print("add_int_header before")

    response = await call_next(request)
    response.headers["X-Integer"] = str(123)

    print("add_int_header after")
    return response


@app.get("/")
async def root():
    print("root")
    return {"message": "Hello World"}
