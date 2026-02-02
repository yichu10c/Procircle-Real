from sqlalchemy import Column, Integer, String
from src.database import Base


class User(Base):
    __tablename__ = "user"

    userId = Column(Integer, primary_key=True, autoincrement=True, index=True)
    firstName = Column(String(255), nullable=False)
    lastName = Column(String(255), nullable=False)

    def __repr__(self):
        return f"<User(userId={self.userId}, firstName='{self.firstName}', lastName='{self.lastName}')>"
