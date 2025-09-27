from fastapi import FastAPI


app = FastAPI()


@app.get("/")
def root_get():
    return {"message": "GET Hello World"}


@app.post("/")
def root_post():
    return {"message": "POST Hello World"}
