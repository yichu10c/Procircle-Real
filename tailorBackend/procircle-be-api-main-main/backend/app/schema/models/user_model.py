import datetime as dt
from sqlalchemy import Column, Integer, String, DateTime
from app.tools.sql import Base


class GuestUser(Base):
    __tablename__ = "guest_user"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    hash = Column(String(100), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: dt.datetime.now(dt.UTC))
