from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db

routers = APIRouter(
    prefix="/chapters"
)

@routers.post('/{id}')
def upload_chapter(id: int, db: Session = Depends(get_db)):
    pass
