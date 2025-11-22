"""
Job Service
"""
from typing import Any, Dict

from app.repository import analysis_query, job_query
from app.tools.sql import connection


class JobService:
    async def get_job_match_details(self, job_match_id: int) -> Dict[str, Any]:
        """
        Get Job Match Details
        """
        async with connection.async_session() as sess:
            return await job_query.get_job_match_detailed_user(sess, job_match_id)

    async def upsert_analysis(self, job_match_id: int, result_asset_id: int, status: int) -> int:
        """
        Update or Insert Analysis Result
        """
        async with connection.async_session() as sess:
            return await analysis_query.upsert_analysis(
                sess, job_match_id, result_asset_id, status
            )

    async def update_job_match_score(self, job_match_id: int, score: float) -> int:
        """
        Update Job Match Score
        """
        async with connection.async_session() as sess:
            return await job_query.update_job_match_score(sess, job_match_id, score)


