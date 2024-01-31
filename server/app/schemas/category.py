from pydantic import BaseModel

class CategorySchema(BaseModel):
    id: int
    cate_name: str

    class Config:
        from_attributes = True

class CreateCategorySchema(BaseModel):
    cate_name: str

    class Config:
        from_attributes = True