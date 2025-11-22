"""
Analyzer Tools
"""
import openai
import json
from typing import Any, Dict, Union

from app.tools.analysis.matcher import calculate_cosine_similarity_score
from job_worker.tools import formatter, prompts
from job_worker.schema.analyze_schema import AnalyzeWpaResult
from tools.observability.log import main_logger as logger
from tools.verdict import get_wpa_verdict


openai_client = openai.AsyncOpenAI()


async def analyze_job_match(
    job_desc_text: str,
    resume_text: str,
    job_title: str = None,
    job_company: str = None,
) -> str:
    """
    Analyze job match by prompting to OpenAI with the output of JSON format

    JSON Content Analysis Result
    ```
    {
        "qualification_analysis": [
            {
                "field": ...,
                "mark": ...,
                "jd": ...,
                "resume": ...,
                "note": ...,
            }
        ],
        "conclusion": ...,
        "area_for_improvement": [
            ...,
            ...,
        ]
    }
    ```
    """
    try:
        # request breakdown analysis
        response = await openai_client.chat.completions.create(
            model="gpt-4o-mini-2024-07-18",
            messages=prompts.generate_job_analysis_prompt_json(job_desc_text, resume_text)
        )
        content = response.choices[0].message.content
        logger.info(content)
        content = content.removeprefix("```json").removesuffix("```")

        # load content JSON from string
        content = json.loads(content)
        content = sanitize_qualification_analysis(content)

        # construct HTML
        matching_score = calculate_matching_score(content)
        cosine_score = calculate_cosine_similarity_score(resume_text, job_desc_text) * 100
        html = formatter.construct_analysis_html(content, job_title, job_company, matching_score, cosine_score)
        logger.info(html)

        return html

    except Exception as error:
        raise error


def calculate_matching_score(content: Dict[str, Any]):
    """
    Matching Score = Count valid qualifications / Total Qualification * 100%

    Note:
    - "\u2714\ufe0f" == '✔'
    """
    qa = content["qualification_analysis"]
    total_row = len(qa)
    total_match = len(list(filter(lambda x: x["mark"] == "\u2714\ufe0f", qa)))
    return total_match / total_row * 100


def sanitize_qualification_analysis(content: Dict[str, Any]):
    """
    Sanitize qualification analysis to remove "N/A" from mark

    Content Format
    ```
    {
        "qualification_analysis": [
            {
                "field": ...,
                "mark": ...,
                "jd": ...,
                "resume": ...,
                "note": ...,
            }
        ],
        "conclusion": ...,
        "area_for_improvement": [
            ...,
            ...,
        ]
    }
    ```
    """
    na_mark = "N/A"
    new_qa = []
    for row in content["qualification_analysis"]:
        if row["mark"] == na_mark and row["jd"] == na_mark and row["resume"] == na_mark:
            continue
        elif row["mark"] == na_mark and row["jd"] == na_mark and row["resume"] != na_mark:
            row["mark"] = "-"
        elif row["mark"] == na_mark and row["jd"] != na_mark and row["resume"] == na_mark:
            row["mark"] = "x"
        new_qa.append(row)
    content["qualification_analysis"] = new_qa
    return content


async def analyze_job_match_wpa(
    job_title: str = None,
    job_desc_text: str = "",
    resume_text: str = "",
) -> AnalyzeWpaResult:
    """
    Analyze job match by prompting to OpenAI with the output of JSON format

    JSON Content Analysis Result
    ```
    {
        "qualification_analysis": [
            {
                "field": ...,
                "mark": ...,
                "jd": ...,
                "resume": ...,
                "note": ...,
                "is_required_by_jobdesc": ...,
                "is_hardskill": ...,
            }
        ],
        "conclusion": ...,
        "area_for_improvement": [
            ...,
            ...,
        ]
    }
    ```
    """
    try:
        # request breakdown analysis
        response = await openai_client.chat.completions.create(
            # model="gpt-4o-mini-2024-07-18",
            # model="gpt-4.1-mini-2025-04-14",
            # model="gpt-4.1-nano-2025-04-14",
            # model="o4-mini-2025-04-16",
            model="gpt-4.1-2025-04-14",
            # reasoning_effort="low",
            messages=prompts.generate_job_analysis_prompt_wpa_json_v2(job_desc_text, resume_text)
        )
        content = response.choices[0].message.content
        logger.info(f"OpenAI Result: \n{content}")

        # load content JSON from string
        content = content.removeprefix("```json").removesuffix("```")
        content = json.loads(content)
        content = sanitize_qualification_analysis(content)

        # validate content keys, if key invalid then proceed retry
        mandatory_parent_fields = {"qualification_analysis", "conclusion", "area_for_improvement"}
        result_fields = set(content.keys())
        missing_fields = mandatory_parent_fields - result_fields
        if (missing_fields):
            logger.warning(f"Incomplete keys returned from OpenAI, missing={missing_fields}, expected={mandatory_parent_fields}, got={result_fields}. Retrying..")
            return await analyze_job_match_wpa(job_title, job_desc_text, resume_text)

        # validate qualifications keys
        mandatory_child_fields = {"mark", "jd", "resume", "note", "is_hardskill", "is_required_by_jobdesc"}
        rows = content["qualification_analysis"]
        if rows:
            result_fields = set(rows[0].keys())
            missing_fields = mandatory_child_fields - result_fields
            if (missing_fields):
                logger.warning(f"Incomplete keys returned from OpenAI, missing={missing_fields}, expected={mandatory_child_fields}, got={result_fields}. Retrying..")
                return await analyze_job_match_wpa(job_title, job_desc_text, resume_text)

        # calculate score
        wpa_score = calculate_wpa_score(content)
        wpa_verdict = get_wpa_verdict(wpa_score)

        # construct HTML
        html = formatter.construct_analysis_wpa_html(content, job_title, wpa_score, wpa_verdict.verdict, wpa_verdict.desc)
        logger.info(f"HTML Content: \n{html}")

        return AnalyzeWpaResult(
            html_content=html,
            wpa_score=wpa_score,
            wpa_verdict=wpa_verdict.verdict,
            wpa_verdict_desc=wpa_verdict.desc
        )

    except Exception as error:
        logger.error(f"Error during analyze job match WPA. error={error}", error)
        raise error


def calculate_wpa_score(content: dict) -> float:
    """
    Content Format
    ```
    {
        "qualification_analysis": [
            {
                "field": ...,
                "mark": ...,
                "jd": ...,
                "resume": ...,
                "note": ...,
                "is_required_by_jobdesc": ...,
                "is_hardskill": ...,
            }
        ],
        "conclusion": ...,
        "area_for_improvement": [
            ...,
            ...,
        ]
    }
    ```

    Note:
    - "\u2714\ufe0f" == '✔'
    """
    numerator = 0
    denominator = 0
    for row in content["qualification_analysis"]:
        qualified = row["mark"] == "\u2714\ufe0f"
        required_by_jd = row["is_required_by_jobdesc"]
        hardskill = row["is_hardskill"]
        if required_by_jd:
            if hardskill:
                numerator += qualified
                denominator += 1
            else:
                numerator += qualified * 0.1
                denominator += 0.1
        else:
            if hardskill:
                numerator += qualified
                denominator += qualified
            else:
                numerator += qualified * 0.1
                denominator += qualified * 0.1
    if denominator:
        return numerator / denominator
    return 0


async def analyze_linkedin_profile(profile_text: str, job_types: str) -> str:
    """Analyze LinkedIn profile and construct a PDF ready HTML"""
    try:
        response = await openai_client.chat.completions.create(
            model="gpt-4o-mini-2024-07-18",
            messages=prompts.generate_profile_analysis_prompt_json(profile_text, job_types),
        )
        content = response.choices[0].message.content
        content = content.removeprefix("```json").removesuffix("```")
        content = json.loads(content)
        html = formatter.construct_profile_html(content, job_types)
        return html
    except Exception as error:
        logger.error(f"Error during analyze_linkedin_profile. {error}")
        raise error
