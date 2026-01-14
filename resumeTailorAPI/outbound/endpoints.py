from fastapi import APIRouter, HTTPException
import os
from openai import OpenAI

router = APIRouter()

@router.post("/api/v1/chat")
async def chat_with_openai():
    """
    Endpoint to send a message to OpenAI and get a response
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY not configured")
    
    try:
        client = OpenAI(api_key=api_key)
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Write my hello world in java"}
            ]
        )
        response_text = completion.choices[0].message.content
        
        return {"response": response_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}")
