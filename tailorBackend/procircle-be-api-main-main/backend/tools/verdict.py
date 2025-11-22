"""
Verdict File
"""

class VerdictDTO:
    def __init__(
        self,
        min_score: float,
        max_score: float,
        verdict: str,
        desc: str,
    ) -> None:
        self.min_score = min_score
        self.max_score = max_score
        self.verdict = verdict
        self.desc = desc

INVALID_VERDICT = VerdictDTO(
    min_score=0.0,
    max_score=0.0,
    verdict="INVALID",
    desc="Invalid Score"
)

STRONG_VERDICT = VerdictDTO(
    min_score=0.8,
    max_score=1.0,
    verdict="STRONG",
    desc="You are highly encouraged to apply."
)

MODERATE_VERDICT = VerdictDTO(
    min_score=0.5,
    max_score=0.8,
    verdict="MODERATE",
    desc="You meet some key qualifications but might need improvement."
)

WEAK_VERDICT = VerdictDTO(
    min_score=0.0,
    max_score=0.5,
    verdict="WEAK",
    desc="Your profile does not strongly align with the job requirements."
)

WPA_VERDICTS = [
    STRONG_VERDICT,
    MODERATE_VERDICT,
    WEAK_VERDICT
]

def get_wpa_verdict(score: float) -> VerdictDTO:
    """
    Get Weight Point Average Verdict
    """
    if not score:
        return WEAK_VERDICT
    for verdict_dto in WPA_VERDICTS:
        if verdict_dto.min_score < score <= verdict_dto.max_score:
            return verdict_dto
    return INVALID_VERDICT
