from typing import Annotated
from fastapi import Depends, FastAPI

app = FastAPI()

# ############################################
# Use dependencies to share the common_parameters for items and users


async def common_parameters(
    q: str | None = None, skip: int = 0, limit: int = 100
) -> dict:
    print(f"common_parameters({q}, {skip}, {limit})")
    return {"q": q, "skip": skip, "limit": limit}


CommonDeps = Annotated[dict, Depends(common_parameters)]


# http GET "http://localhost:8000/items/?q=%22qqq%22&skip=1&limit=20"
@app.get("/items/")
async def read_items(commons: CommonDeps):
    print("read_items")
    return commons


@app.get("/users/")
async def read_users(commons: CommonDeps):
    print("read_users")
    return commons
