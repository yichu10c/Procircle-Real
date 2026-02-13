from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from src.database import Base


class User(Base):
    __tablename__ = "user"

    userId = Column(Integer, primary_key=True, autoincrement=True, index=True)
    firstName = Column(String(255), nullable=False)
    lastName = Column(String(255), nullable=False)
    createdAt = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    def __repr__(self):
        return f"<User(userId={self.userId}, firstName='{self.firstName}', lastName='{self.lastName}')>"
