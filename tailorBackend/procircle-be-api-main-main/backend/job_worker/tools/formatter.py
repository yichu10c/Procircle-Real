"""
HTML Formatter
"""
import datetime as dt
from typing import Any, Dict, List


def format_day(day: int) -> str:
    """Return a day of month with its ordinal suffix."""
    if 10 <= day % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
    return f"{day}{suffix}"


def construct_analysis_html(
    content: Dict[str, Any],
    job_title: str,
    job_company: str,
    matching_score: float,
    cosine_score: float,
):
    """
    Construct HTML docs with analysis result as content
    """
    style = construct_style()
    metadata = construct_analysis_metadata(job_title, job_company, matching_score, cosine_score)
    qualification_analysis = construct_qualification_analysis(content["qualification_analysis"])
    conclusion = construct_conclusion(content["conclusion"])
    area_for_improvement = construct_area_for_improvement(content["area_for_improvement"])
    return (
        "\n<!DOCTYPE html>"
        '\n<html lang="en">'
        "\n<head>"
        '\n    <meta charset="UTF-8">'
        '\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">'
        "\n    <title>Job Match Analysis</title>"
        f"\n{style}"
        "\n</head>"
        "\n<body>"
        "\n"
        "\n<h1>Job Match Analysis</h1>"
        "\n"
        f"\n{metadata}" #metadata
        "\n"
        f"\n{qualification_analysis}" #table
        "\n"
        f"\n{conclusion}" #conclusion
        "\n"
        f"\n{area_for_improvement}" #area for improvement
        "\n"
        "\n</body>"
        "\n</html>"
    )


def construct_analysis_wpa_html(
    content: Dict[str, Any],
    job_title: str,
    wpa_score: float,
    wpa_verdict: str,
    wpa_verdict_desc: str,
):
    """
    Construct HTML docs with analysis result as content
    """
    style = construct_style()
    metadata = construct_analysis_wpa_metadata(job_title)
    # qualification_analysis = construct_qualification_analysis(content["qualification_analysis"])
    qualification_analysis = construct_qualification_wpa_analysis(content["qualification_analysis"])
    # conclusion = construct_conclusion(content["conclusion"])
    conclusion = construct_conclusion_wpa(content["conclusion"], wpa_score, wpa_verdict, wpa_verdict_desc)
    area_for_improvement = construct_area_for_improvement(content["area_for_improvement"])
    return (
        "\n<!DOCTYPE html>"
        '\n<html lang="en">'
        "\n<head>"
        '\n    <meta charset="UTF-8">'
        '\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">'
        "\n    <title>Job Match Analysis</title>"
        f"\n{style}"
        "\n</head>"
        "\n<body>"
        "\n"
        "\n<h1>Job Match Analysis</h1>"
        "\n"
        f"\n{metadata}" #metadata
        "\n"
        f"\n{qualification_analysis}" #table
        "\n"
        f"\n{conclusion}" #conclusion
        "\n"
        f"\n{area_for_improvement}" #area for improvement
        "\n"
        "\n</body>"
        "\n</html>"
    )


def construct_style():
    """
    Construct CSS for HTML
    """
    return """
    <style>
        /* Set the page size to A4 for printing */
        @page {
            size: A4;
            width: 210mm;
            height: 297mm;
            margin: auto;
            box-sizing: border-box;
            background: white;
            border: 1px solid #ddd;
            position: relative;
            display: flex;
            flex-direction: column;
        }

        @media print {
            .page {
                page-break-before: always;
            }
        }

        /* Reset body margins and ensure full height for A4 */
        body {
            margin: 10mm;
            padding: 10mm;
            font-family: Arial, sans-serif;
            background-color: #fff;
        }

        /* Core Format */
        h1 {
            text-align: center;
        }
        h2 {
            text-align: left;
        }
        p {
            text-align: justify;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }
        th, td {
            border: 1px solid black;
            padding: 8px;
            text-align: left;
        }
    </style>
    """


def construct_analysis_metadata(
    job_title: str,
    job_company: str,
    matching_score: float,
    cosine_score: float,
):
    """
    Construct analysis document metadata containing
    - job title (if any)
    - company (if any)
    - generated time
    """
    # construct generated time
    current_date = dt.datetime.now()
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    day = format_day(current_date.day)
    month = months[current_date.month - 1]
    format_time = lambda x: f"0{x}" if len(str(x)) == 1 else str(x)
    hour = format_time(current_date.hour)
    minute = format_time(current_date.minute)
    second = format_time(current_date.second)
    generated_time = f"{month} {day} {current_date.year}. {hour}:{minute}:{second}. (UTC)"

    # normalize matching score
    matching_score = f"{matching_score:.2f}%"
    cosine_score = f"{cosine_score:.2f}%"

    # construct metadata
    metadata = []
    if job_title:
        metadata.append(f"<p><strong>Job Title:</strong> {job_title} </p>")
    if job_company:
        metadata.append(f"<p><strong>Company:</strong> {job_company} </p>")
    metadata.append(f"<p><strong>Matching Score:</strong> {matching_score} </p>")
    metadata.append(f"<p><strong>Cosine Score:</strong> {cosine_score} </p>")

    metadata.append(f"<p><strong>Generated Time:</strong> {generated_time} </p>")

    metadata = "\n".join(metadata)
    return metadata


def construct_analysis_wpa_metadata(job_title: str):
    """
    Construct analysis document metadata containing
    - job title (if any)
    - company (if any)
    - generated time
    """
    # construct generated time
    current_date = dt.datetime.now()
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    day = format_day(current_date.day)
    month = months[current_date.month - 1]
    format_time = lambda x: f"0{x}" if len(str(x)) == 1 else str(x)
    hour = format_time(current_date.hour)
    minute = format_time(current_date.minute)
    second = format_time(current_date.second)
    generated_time = f"{month} {day} {current_date.year}. {hour}:{minute}:{second}. (UTC)"

    # construct metadata
    metadata = []
    if job_title:
        metadata.append(f"<p><strong>Job Title:</strong> {job_title} </p>")
    metadata.append(f"<p><strong>Generated Time:</strong> {generated_time} </p>")

    metadata = "\n".join(metadata)
    return metadata


def construct_qualification_analysis(rows: List[Dict[str, str]]) -> str:
    """
    Construct qualification analysis HTML

    rows
    {
        "field": ...
        "mark": ...
        "jd": ...
        "resume": ...
        "note": ...
    }

    <h2>Qualification Analysis</h2>
    <table>
        <tr>
            <th>FIELD</th>
            <th>MARK</th>
            <th>JOB DESC</th>
            <th>RESUME</th>
            <th>NOTE</th>
        </tr>
        <tr>
            <td>Job Title</td>
            <td>x</td>
            <td>Senior Software Engineer (Back End)</td>
            <td>N/A</td>
            <td>Position not matched; the resume does not apply for a related title.</td>
        </tr>
    </table>
    """
    table_row = []
    for row in rows:
        html_row = (
            "\n<tr>"
            f"\n    <td>{row['field']}</td>"
            f"\n    <td>{row['mark']}</td>"
            f"\n    <td>{row['jd']}</td>"
            f"\n    <td>{row['resume']}</td>"
            f"\n    <td>{row['note']}</td>"
            "\n</tr>"
        )
        table_row.append(html_row)

    table_html = '\n'.join(table_row)

    return (
        "\n<h2>Qualification Analysis</h2>"
        "\n<table>"
        "\n    <tr>"
        "\n        <th>FIELD</th>"
        "\n        <th>MARK</th>"
        "\n        <th>JOB DESC</th>"
        "\n        <th>RESUME</th>"
        "\n        <th>NOTE</th>"
        "\n    </tr>"
        f"\n{table_html}"
        "\n</table>"
    )


def construct_qualification_wpa_analysis(rows: List[Dict[str, str]]) -> str:
    """
    Construct qualification analysis HTML

    rows
    {
        "field": ...
        "mark": ...
        "jd": ...
        "resume": ...
        "note": ...
        "is_required_by_jobdesc": ...
        "is_hardskill": ...
    }

    <h2>Qualification Analysis</h2>
    <table>
        <tr>
            <th>FIELD</th>
            <th>MARK</th>
            <th>JOB DESC</th>
            <th>RESUME</th>
            <th>NOTE</th>
            <th>REQUIRED</th>
            <th>SKILL CATEGORY</th>
        </tr>
        <tr>
            <td>Job Title</td>
            <td>x</td>
            <td>Senior Software Engineer (Back End)</td>
            <td>N/A</td>
            <td>Position not matched; the resume does not apply for a related title.</td>
        </tr>
    </table>

    Note:
    - "\u2714\ufe0f" == '✔'
    """
    table_row = []
    for row in rows:
        is_required = "✔" if row["is_required_by_jobdesc"] else "x"
        skill_category = "Hard Skill" if row["is_hardskill"] else "Soft Skill"
        html_row = (
            "\n<tr>"
            f"\n    <td>{row['field']}</td>"
            f"\n    <td>{row['mark']}</td>"
            f"\n    <td>{row['jd']}</td>"
            f"\n    <td>{row['resume']}</td>"
            f"\n    <td>{row['note']}</td>"
            f"\n    <td>{is_required}</td>"
            f"\n    <td>{skill_category}</td>"
            "\n</tr>"
        )
        table_row.append(html_row)

    table_html = '\n'.join(table_row)

    return (
        "\n<h2>Qualification Analysis</h2>"
        "\n<table>"
        "\n    <tr>"
        "\n        <th>FIELD</th>"
        "\n        <th>MARK</th>"
        "\n        <th>JOB DESC</th>"
        "\n        <th>RESUME</th>"
        "\n        <th>NOTE</th>"
        "\n        <th>REQUIRED</th>"
        "\n        <th>SKILL CATEGORY</th>"
        "\n    </tr>"
        f"\n{table_html}"
        "\n</table>"
    )


def construct_conclusion(conclusion: str):
    """
    Construct conclusion HTML content

    e.g.
    <h2>Conclusion</h2>
    <p>The qualifications listed in the resume do not align with the requirements stated in the job description for the Senior Software Engineer position at Capital One. Key areas such as necessary education, relevant experience, and technical skills are lacking.</p>
    """
    return (
        "\n<h2>Conclusion</h2>"
        f"\n<p>{conclusion}</p>"
    )


def construct_conclusion_wpa(
    conclusion: str,
    wpa_score: float,
    wpa_verdict: str,
    wpa_verdict_desc: str
):
    """
    Construct conclusion HTML content

    e.g.
    <h2>Conclusion</h2>
    <p>The qualifications listed in the resume do not align with the requirements stated in the job description for the Senior Software Engineer position at Capital One. Key areas such as necessary education, relevant experience, and technical skills are lacking.</p>
    """
    wpa_score = f"{(wpa_score * 100):.2f}%"
    wpa_verdict_text = f"({wpa_verdict}) {wpa_verdict_desc}"
    return (
        "\n<h2>Conclusion</h2>"
        f"\n<p>{conclusion}</p>"
        f"<p><strong>Matching Score:</strong> {wpa_score} </p>"
        f"<p><strong>Analysis Result:</strong> {wpa_verdict_text} </p>"
    )


def construct_area_for_improvement(points: List[str]):
    """
    <h2>Area for Improvement</h2>
    <ul>
        <li>Consider pursuing relevant coursework or a degree in computer science or a related field to fulfill educational requirements.</li>
        <li>Gain practical experience through internships or projects related to software engineering to build a foundational experience.</li>
        <li>Familiarize yourself with relevant programming languages and cloud services by taking online courses or participating in coding bootcamps.</li>
        <li>Engage in projects that utilize Agile practices and open-source frameworks to demonstrate familiarity and proficiency.</li>
        <li>Develop a technical portfolio that showcases software projects and programming skills, which can significantly enhance job applications.</li>
    </ul>
    """
    html_points = [f"    <li>{point}</li>" for point in points]
    html_text = "\n".join(html_points)

    return (
        f"\n<h2>Area for Improvement</h2>"
        f"\n<ul>"
        f"\n{html_text}"
        f"\n</ul>"
    )


def construct_profile_metadata(job_types: str) -> str:
    """Construct metadata for LinkedIn profile analysis"""
    current_date = dt.datetime.now()
    months = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]
    day = format_day(current_date.day)
    month = months[current_date.month - 1]
    format_time = lambda x: f"0{x}" if len(str(x)) == 1 else str(x)
    hour = format_time(current_date.hour)
    minute = format_time(current_date.minute)
    second = format_time(current_date.second)
    generated_time = f"{month} {day} {current_date.year}. {hour}:{minute}:{second}. (UTC)"

    metadata = [f"<p><strong>Target Job Types:</strong> {job_types}</p>"]
    metadata.append(f"<p><strong>Generated Time:</strong> {generated_time} </p>")
    return "\n".join(metadata)


def construct_profile_analysis(rows: List[Dict[str, str]]) -> str:
    """Construct LinkedIn profile analysis table"""
    table_row = []
    for row in rows:
        html_row = (
            "\n<tr>"
            f"\n    <td>{row['field']}</td>"
            f"\n    <td>{row['note']}</td>"
            "\n</tr>"
        )
        table_row.append(html_row)
    table_html = "\n".join(table_row)
    return (
        "\n<h2>Profile Analysis</h2>"
        "\n<table>"
        "\n    <tr>"
        "\n        <th>FIELD</th>"
        "\n        <th>NOTE</th>"
        "\n    </tr>"
        f"\n{table_html}"
        "\n</table>"
    )


def construct_profile_html(content: Dict[str, Any], job_types: str) -> str:
    """Construct final HTML for LinkedIn profile analysis"""
    style = construct_style()
    metadata = construct_profile_metadata(job_types)
    analysis = construct_profile_analysis(content["analysis"])
    conclusion = construct_conclusion(content.get("conclusion", ""))
    return (
        "\n<!DOCTYPE html>"
        '\n<html lang="en">'
        "\n<head>"
        '\n    <meta charset="UTF-8">'
        '\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">'
        "\n    <title>LinkedIn Profile Analysis</title>"
        f"\n{style}"
        "\n</head>"
        "\n<body>"
        "\n"
        "\n<h1>LinkedIn Profile Analysis</h1>"
        "\n" f"\n{metadata}"
        "\n" f"\n{analysis}"
        "\n" f"\n{conclusion}"
        "\n" "\n</body>" "\n</html>"
    )




def construct_simple_html(content: str) -> str:
    """Construct very simple HTML document from plain text."""
    style = construct_style()
    body = content.replace("\n", "<br />")
    return (
        "\n<!DOCTYPE html>"
        '\n<html lang="en">'
        "\n<head>"
        '\n    <meta charset="UTF-8">'
        '\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">'
        f"\n{style}"
        "\n</head>"
        "\n<body>"
        f"\n<p>{body}</p>"
        "\n</body>"
        "\n</html>"
    )
