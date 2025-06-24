from sqlalchemy import (
    Integer,
    String,
    Boolean,
    DateTime,
    Text,
    ForeignKey,
    JSON
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)
from typing import List, Optional
from datetime import datetime


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[Optional[str]] = mapped_column(String(255))
    vk_id: Mapped[Optional[str]] = mapped_column(String(255))
    tg_username: Mapped[Optional[str]] = mapped_column(String(255))
    firstname: Mapped[Optional[str]] = mapped_column(String(255))
    lastname: Mapped[Optional[str]] = mapped_column(String(255))
    is_museum_worker: Mapped[Optional[bool]] = mapped_column(Boolean, default=False)
    museum: Mapped[Optional[str]] = mapped_column(String(255))
    occupation: Mapped[Optional[str]] = mapped_column(String(255))
    registration_date: Mapped[Optional[DateTime]] = mapped_column(
        DateTime,
        default=datetime.now()
    )
    course_subscribe: Mapped[Optional[int]] = mapped_column(
        ForeignKey("courses.id")
    )
    is_admin: Mapped[Optional[bool]] = mapped_column(Boolean, default=False)

    stories: Mapped[List["Story"]] = relationship(
        "Story", back_populates="user"
    )
    questions: Mapped[List["UserQuestion"]] = relationship(
        "UserQuestion", back_populates="user"
    )
    course_progress: Mapped[List["UserCourseProgress"]] = relationship(
        "UserCourseProgress", back_populates="user"
    )
    story_history: Mapped[List["StoryHistory"]] = relationship(
        "StoryHistory", back_populates="user"
    )
    subscribed_course: Mapped[Optional["Course"]] = relationship(
        "Course", foreign_keys=[course_subscribe]
    )


class Story(Base):
    __tablename__ = "stories"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("user.id"),
        nullable=True
    )
    user_name: Mapped[Optional[str]] = mapped_column(String(255))
    updated: Mapped[Optional[DateTime]] = mapped_column(
        DateTime,
        default=datetime.now(),
        onupdate=datetime.now()
    )
    created: Mapped[Optional[DateTime]] = mapped_column(
        DateTime,
        default=datetime.now(),
        onupdate=datetime.now()
    )
    status: Mapped[Optional[str]] = mapped_column(String(50))
    content_type: Mapped[Optional[str]] = mapped_column(String(50))
    title: Mapped[Optional[str]] = mapped_column(String(255))
    text: Mapped[Optional[str]] = mapped_column(Text)
    tag: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    media_url: Mapped[Optional[str]] = mapped_column(String(500))
    link: Mapped[Optional[str]] = mapped_column(String(500))
    is_anonymous: Mapped[Optional[bool]] = mapped_column(Boolean, default=False)
    is_agreed_to_publication: Mapped[Optional[bool]] = mapped_column(Boolean, default=False)

    user: Mapped[Optional["User"]] = relationship(
        "User", back_populates="stories"
    )
    questions: Mapped[List["UserQuestion"]] = relationship(
        "UserQuestion", back_populates="story"
    )
    history: Mapped[List["StoryHistory"]] = relationship(
        "StoryHistory", back_populates="story"
    )


class UserQuestion(Base):
    __tablename__ = "user_questions"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("user.id"))
    story_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("stories.id"), nullable=True)
    question: Mapped[Optional[str]] = mapped_column(Text)
    answer: Mapped[Optional[str]] = mapped_column(Text)
    parent_id: Mapped[Optional[int]] = mapped_column(Integer)
    question_date: Mapped[Optional[DateTime]] = mapped_column(
        DateTime,
        default=datetime.now()
    )
    answer_date: Mapped[Optional[DateTime]] = mapped_column(
        DateTime,
        default=datetime.now()
    )
    viewed: Mapped[Optional[DateTime]] = mapped_column(DateTime, default=datetime.now())

    user: Mapped[Optional["User"]] = relationship(
        "User", back_populates="questions"
    )
    story: Mapped[Optional["Story"]] = relationship(
        "Story", back_populates="questions"
    )


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(primary_key=True)
    course_name: Mapped[Optional[str]] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(Text)

    parts: Mapped[List["CoursePart"]] = relationship(
        "CoursePart", back_populates="course"
    )


class CoursePart(Base):
    __tablename__ = "course_part"

    id: Mapped[int] = mapped_column(primary_key=True)
    course_id: Mapped[Optional[int]] = mapped_column(ForeignKey("courses.id"))
    order_number: Mapped[Optional[int]] = mapped_column(Integer)
    title: Mapped[Optional[str]] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(Text)
    video_url: Mapped[Optional[str]] = mapped_column(String(500))
    question: Mapped[Optional[str]] = mapped_column(Text)

    course: Mapped[Optional["Course"]] = relationship(
        "Course", back_populates="parts"
    )
    progress: Mapped[List["UserCourseProgress"]] = relationship(
        "UserCourseProgress", back_populates="part"
    )


class UserCourseProgress(Base):
    __tablename__ = "user_course_progress"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("user.id"))
    part_id: Mapped[Optional[int]] = mapped_column(ForeignKey("course_part.id"))
    date: Mapped[Optional[DateTime]] = mapped_column(DateTime)
    answer: Mapped[Optional[str]] = mapped_column(Text)

    user: Mapped[Optional["User"]] = relationship(
        "User", back_populates="course_progress"
    )
    part: Mapped[Optional["CoursePart"]] = relationship(
        "CoursePart", back_populates="progress"
    )


class StoryHistory(Base):
    __tablename__ = "story_history"

    id: Mapped[int] = mapped_column(primary_key=True)
    story_id: Mapped[Optional[int]] = mapped_column(ForeignKey("stories.id"))
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("user.id"))
    date: Mapped[Optional[DateTime]] = mapped_column(DateTime)

    user: Mapped[Optional["User"]] = relationship(
        "User", back_populates="story_history"
    )
    story: Mapped[Optional["Story"]] = relationship(
        "Story", back_populates="history"
    )
