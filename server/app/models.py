from .database import Base
from sqlalchemy import Column, String, TIMESTAMP, Integer, text, Boolean, ForeignKey, ARRAY
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False, server_default="student")
    education = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))

class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True, nullable=False)
    cate_name = Column(String, nullable=False)


class Course(Base):
    # TODO: add the summary column, course_duration column. 
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True, nullable=False)
    course_name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    teacher = Column(String, nullable=False)
    img_url = Column(String, nullable=True, server_default=None)
    is_published = Column(Boolean, nullable=False, server_default="True")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at = Column(String, nullable=True)
    course_code = Column(String, nullable=False)
    category = Column(Integer, ForeignKey("category.id", ondelete="CASCADE", name="category_fk"), nullable=False)

class Enrollments(Base):
    __tablename__ = "enrollments"

    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), primary_key=True) # type: ignore
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    enroll_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    completed_chapters = Column(ARRAY(Integer), nullable=True)
    is_completed = Column(Boolean, nullable=True, server_default="False")

class Chapters(Base):
    __tablename__ = "chapters"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    chapter_no = Column(Integer, nullable=False)
    video_url = Column(String, nullable=True)
    resources_url = Column(String, nullable=True)
    is_published = Column(Boolean, nullable=False, server_default="False")
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE", name="course_fk"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))

class Ratings(Base):

    __tablename__ = "ratings"
    id = Column(Integer, primary_key=True, nullable=False)
    course = Column(Integer, ForeignKey("courses.id",ondelete="CASCADE", name="course_rating_fk"), nullable=False)
    user = Column(Integer, ForeignKey("users.id", ondelete="CASCADE", name="user_rating_fk"), nullable=False)
    rating = Column(Integer, nullable=False, server_default="1")
    remarks = Column(String, nullable=True)
    