"""
Job Worker Constant
"""

class JobAnalysisStatus:
    SUCCESS = 1
    FAILED_RETRYABLE = 0
    FAILED_NON_RETRYABLE = -1
