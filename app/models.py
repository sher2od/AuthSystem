from sqlalchemy import(
    Column,
    Integer,
    Text,
    String,
    Boolean,ForeignKey
)

from sqlalchemy.orm import relationship

from .database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer,primary_key=True,index=True)
    first_name = Column(String(64),nullable=False)
    last_name = Column(String(64))
    email = Column(String(256),unique=True,nullable=False)
    hashed_password = Column(String(512),nullable=False)
    is_active = Column(Boolean,default=False)
    is_verified = Column(Boolean,default=False)
    verification_code = Column(Integer)

    tasks = relationship("Task",back_populates="user")



    @property
    def full_name(self) -> str:
        if self.last_name:
            return f"{self.first_name} {self.last_name}"
        else:
            return self.first_name
        
    def __repr__(self):
        return f"{self.first_name}:{self.email} - {self.full_name}"
        
class Task(Base):
    __tablename__ = "tasks"

    task_id = Column(Integer,primary_key=True,index=True)
    title = Column(String,nullable=False)
    description = Column(Text)
    user_id = Column(ForeignKey("users.user_id",ondelete="CASCADE"))

    user = relationship("User",back_populates="tasks")

    def __repr__(self):
        return f"{self.task_id}: {self.title} - {self.user.full_name}"