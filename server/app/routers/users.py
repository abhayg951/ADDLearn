from .. import models
from ..schemas import user, enrollment
from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from ..oauth2 import get_current_user
from sqlalchemy import func

routers = APIRouter(
    prefix="/user",
    tags=["User"]
)


@routers.get("/me", response_model=user.UserResponse)
def current_user(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    user = db.query(models.User).filter(models.User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id {id} does not exist")
    return user

@routers.get('/me/courses')
def user_enrollments(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    # user_enrolls = db.query(models.User.id, models.Enrollments.course_id, models.Enrollments.enroll_at).outerjoin(models.Enrollments, models.User.id == models.Enrollments.user_id).filter(models.User.id == current_user.id).all()
    # result_dict = [{'user_id': user_id, 'course_id': course_id, 'enroll_at': enroll_at} for user_id, course_id, enroll_at in user_enrolls]
    user_enroll = db.query(models.Enrollments).filter(models.Enrollments.user_id == current_user.id).all()
    return user_enroll

#TODO: create the user single enrollment 
@routers.get('/me/courses/{cid}', response_model=enrollment.EnrollmentSchema)
def user_single_enrollment(cid: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    ''' this will show user's single enrollment '''
    single_enroll = db.query(models.Enrollments).filter(models.Enrollments.user_id == current_user.id, models.Enrollments.course_id == cid)
    if not single_enroll.first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not enrolled")
    return single_enroll.first()