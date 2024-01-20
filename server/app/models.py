from .database import Base
from sqlalchemy import Column, String, TIMESTAMP, Integer, text, Boolean, ForeignKey
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
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True, nullable=False)
    course_name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    img_url = Column(String, nullable=False)
    is_published = Column(Boolean, nullable=False, server_default="True")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at = Column(String, nullable=True)
    course_code = Column(String, nullable=False)
    category = Column(Integer, ForeignKey("category.id", ondelete="CASCADE", name="category_fk"), nullable=False)

class Enrollments(Base):
    __tablename__ = "enrollments"

    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    enroll_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))