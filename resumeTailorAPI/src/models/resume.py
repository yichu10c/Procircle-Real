from sqlalchemy import Column, Integer, String, Text, ForeignKey
from src.database import Base


class Resume(Base):
    __tablename__ = "resume"

    resumeId = Column(Integer, primary_key=True, autoincrement=True, index=True)
    userId = Column(Integer, ForeignKey("user.userId"), nullable=False, index=True)
    fileName = Column(String(255), nullable=True)  # Original file name if uploaded as .docx
    resumeText = Column(Text, nullable=False)  # The resume content as text
    fileType = Column(String(50), nullable=False, default="text")  # "text", "docx", etc.

    def __repr__(self):
        return f"<Resume(resumeId={self.resumeId}, userId={self.userId}, fileName='{self.fileName}', fileType='{self.fileType}')>"
