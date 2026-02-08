from sqlalchemy import Column, Integer, String, Text, ForeignKey
from src.database import Base


class Resume(Base):
    __tablename__ = "resume"

    resumeId = Column(Integer, primary_key=True, autoincrement=True, index=True)
    userId = Column(Integer, ForeignKey("user.userId"), nullable=False, index=True)
    fileName = Column(String(255), nullable=False)
    resumeText = Column(Text, nullable=False)

    def __repr__(self):
        return f"<Resume(resumeId={self.resumeId}, userId={self.userId}, fileName='{self.fileName}')>"
