from fastapi import Depends, status, APIRouter, HTTPException
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import schemas, database, utils, models, oauth2
from datetime import datetime, timedelta, timezone
from starlette.responses import Response

routers = APIRouter(
    tags=["Authentication"]
)


@routers.post("/sign-in", response_model=schemas.Token)
def login(response: Response, user_credential: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    user = db.query(models.User).filter(models.User.email == user_credential.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    
    if not utils.verify(user_credential.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    # create token
    access_token= oauth2.create_access_token(data = {"user_id": user.id})
    # set cookie
    expires = datetime.now(timezone.utc) + timedelta(hours=6, minutes=30)
    response.set_cookie(key="access_token", value=access_token, secure=True, expires=expires)
    # return token
    return {"access_token": access_token, "token_type": "bearer"}


@routers.post("/sign-up", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):

    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"email already been taken")

    # hash the password = user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
