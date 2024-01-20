from fastapi import APIRouter

routers = APIRouter(
    prefix="/category",
    tags=["Category"]
)

# @routers.post("")
# def create_category():
