from pydantic import BaseModel

class AnalyzeWpaResult(BaseModel):
    html_content: str
    wpa_score: float
    wpa_verdict: str
    wpa_verdict_desc: str
