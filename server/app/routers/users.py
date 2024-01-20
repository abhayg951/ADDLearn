from .. import schemas, models, utils
from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from ..oauth2 import get_current_user
from sqlalchemy import func

routers = APIRouter(
    prefix="/user",
    tags=["User"]
)


@routers.get("/me", response_model=schemas.UserResponse)
def current_user(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    user = db.query(models.User).filter(models.User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id {id} does not exist")
    return user
