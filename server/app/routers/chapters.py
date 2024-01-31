from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..oauth2 import get_current_user
from ..cloudinary import uploadfile

routers = APIRouter(
    prefix="/chapters"
)

@routers.post('/{id}')
def upload_chapter(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    
    pass
