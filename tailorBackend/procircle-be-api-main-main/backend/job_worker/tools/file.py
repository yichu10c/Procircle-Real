"""
Localfile Handler
"""
import datetime as dt
import os
from uuid import uuid4

import boto3
import docx
import requests
import pdfkit

from tools.aws import s3
from tools.observability.log import main_logger as logger


def safe_remove_file(filepath: str):
    """
    Safely remove temporary file
    """
    try:
        os.remove(filepath)
    except:
        pass


async def handle_upload_pdf(content: str, user_hash: str, prefix: str = "job-match-analysis") -> str:
    """Handle PDF file upload

    Parameters
    ----------
    content: str
        HTML content to be converted to PDF.
    user_hash: str
        Unique user hash used for generating the upload path.
    prefix: str, optional
        Prefix for the generated PDF filename. Defaults to "job-match-analysis".
    """
    # handle local file
    os.makedirs(".temp", exist_ok=True)
    datestring = (
        dt.datetime.now(dt.UTC)
        .isoformat()[:-6]
        .replace("T", "_")
        .replace(":", "")
        .replace(".", "_")
    )
    filename = f"{prefix}-{datestring}.pdf"
    filepath = f".temp/{filename}"

    # write to pdf
    pdfkit.from_string(content, filepath)

    # upload to s3
    download_url = s3.upload_file(filepath, f"analysis/{user_hash}/{filename}")

    # remove local file
    safe_remove_file(filepath)

    return download_url


def extract_docx_from_url(url: str) -> str:
    """
    Extract docx file content from provider URL
    """
    filepath = ""

    try:
        os.makedirs(".temp")
    except:
        pass

    try:
        # construct path
        file_ext = url.split(".")[-1]
        filepath = f".temp/{uuid4().hex}.{file_ext}"

        # download and write
        response = requests.get(url)
        with open(filepath, "wb") as file:
            file.write(response.content)

        # parse docx file
        document = docx.Document(filepath)
        document_text = "\n".join([par.text for par in document.paragraphs])

        return document_text

    except Exception as error:
        logger.error(f"failed when extracting external document. {url=} {filepath=} {error=}")
        raise error

    finally:
        safe_remove_file(filepath)
