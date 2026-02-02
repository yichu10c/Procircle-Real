from fastapi import UploadFile, HTTPException
from docx import Document
from typing import Optional
import os


class ResumeProcessor:
    """Handles resume file and text processing"""

    @staticmethod
    def validate_inputs(resume_text: Optional[str], resume_file: Optional[UploadFile]) -> None:
        """Validate that exactly one resume input is provided"""
        if not resume_text and not resume_file:
            raise HTTPException(
                status_code=400,
                detail="Provide either resume_text or resume_file"
            )
        
        if resume_text and resume_file:
            raise HTTPException(
                status_code=400,
                detail="Provide either resume_text OR resume_file, not both"
            )

    @staticmethod
    async def extract_text_from_file(resume_file: UploadFile) -> str:
        """Extract text from a .docx file"""
        if not resume_file.filename.endswith(".docx"):
            raise HTTPException(
                status_code=400, 
                detail="Only .docx files are supported."
            )
        
        try:
            contents = await resume_file.read()
            temp_path = "temp_resume.docx"
            
            with open(temp_path, "wb") as f:
                f.write(contents)
            
            doc = Document(temp_path)
            resume_text = "\n".join([para.text for para in doc.paragraphs])
            
            # Clean up temp file
            if os.path.exists(temp_path):
                os.remove(temp_path)
            
            return resume_text
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail=f"Failed to process file: {e}"
            )

    @staticmethod
    async def get_resume_text(
        resume_text: Optional[str], 
        resume_file: Optional[UploadFile]
    ) -> str:
        """Get resume text from either text input or file upload"""
        ResumeProcessor.validate_inputs(resume_text, resume_file)
        
        if resume_file:
            return await ResumeProcessor.extract_text_from_file(resume_file)
        
        return resume_text
