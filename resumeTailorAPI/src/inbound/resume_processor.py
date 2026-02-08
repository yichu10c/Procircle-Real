from fastapi import UploadFile, HTTPException
from docx import Document
from sqlalchemy.orm import Session
from src.models import Resume
import io


class ResumeProcessor:

    @staticmethod
    async def extract_text_from_upload(resume_file: UploadFile) -> str:
        if not resume_file.filename.endswith(".docx"):
            raise HTTPException(
                status_code=400,
                detail="Only .docx files are supported."
            )

        try:
            contents = await resume_file.read()
            doc = Document(io.BytesIO(contents))
            return "\n".join([para.text for para in doc.paragraphs])
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to extract text from file: {e}"
            )

    @staticmethod
    async def save_resume_to_db(
        user_id: int,
        resume_file: UploadFile,
        db: Session
    ) -> Resume:
        resume_text = await ResumeProcessor.extract_text_from_upload(resume_file)

        new_resume = Resume(
            userId=user_id,
            fileName=resume_file.filename,
            resumeText=resume_text
        )
        db.add(new_resume)
        db.commit()
        db.refresh(new_resume)

        return new_resume
