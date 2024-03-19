from fastapi import Response, APIRouter, Depends
from database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    tags=["Course Rating"]
    prefix="/rating"
)

@router.post("/{course_id}")
def rate_course(current_user: Session = Depends(get_db)):
    pass

# @routers.post("/{course_id}/rate")
# def rate_course(course_id: int,
#                 rate_schema: courses.RateCourseSchema, 
#                 db: Session = Depends(get_db),
#                 current_user: models.User = Depends(oauth2.get_current_user)):
    
#     get_enroll = db.query(models.Enrollments).filter(models.Enrollments.user_id == current_user.id)
#     if not get_enroll.first():
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You must enroll in the course")
    
#     # check enrollment

#     return current_user