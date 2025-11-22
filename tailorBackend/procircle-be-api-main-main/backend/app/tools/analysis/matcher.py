"""
Job Matching Handler
"""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_cosine_similarity_score(
    resume_text: str,
    job_desc_text: str
) -> float:
    """
    Calculate cosine similarity score
    - 3 vectorizer are used to determine the score between 2 texts
    - all vectors from vectorizer then combined and find the average to get the average score
    """
    feature_vectorizer = TfidfVectorizer()
    score = cosine_similarity(
        feature_vectorizer.fit_transform(
            [resume_text, job_desc_text]
        )
    )[0][1]
    return score
