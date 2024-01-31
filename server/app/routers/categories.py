from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..schemas import category
from .. import oauth2, database, models

routers = APIRouter(
    prefix="/category",
    tags=["Category"]
)

@routers.get("", response_model=List[category.CategorySchema], status_code=status.HTTP_200_OK)
def get_categories(db: Session = Depends(database.get_db)):
    get_cate = db.query(models.Category).all()
    return get_cate

@routers.post("", response_model=category.CategorySchema)
def create_category(input_info: category.CreateCategorySchema, 
                    db: Session = Depends(database.get_db), 
                    current_user: models.User = Depends(oauth2.get_current_user)):
    
    if str(current_user.role) != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="you are not allowed to create a category")
    
    new_category = models.Category(**input_info.model_dump())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category