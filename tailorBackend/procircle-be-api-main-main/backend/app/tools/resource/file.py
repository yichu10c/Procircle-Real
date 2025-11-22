"""
Localfile Handler
"""
import docx
import os
from uuid import uuid4

import requests
from fastapi import UploadFile
from tools.observability.log import main_logger as logger


class FileHandler:
    """
    One time use local file handler
    """
    temp_dir = "./.temp"

    def __init__(self) -> None:
        self.localpaths = []

    def __enter__(self):
        self.initialize_temp_dir()
        return self

    def __exit__(self, *args):
        if not self.localpaths:
            return

        for path in self.localpaths:
            try:
                os.remove(path)
            except Exception as error:
                logger.error(f"got exception during remove temp file {path}. {error=}")

    def initialize_temp_dir(self):
        try:
            if not self.temp_dir in os.listdir():
                os.mkdir(".temp")
        except FileExistsError:
            pass
        except Exception as error:
            logger.error(f"got exception during initialize temp dir. {error=}")


class UploadFileHandler(FileHandler):
    """
    """
    def __init__(self) -> None:
        super().__init__()

    def temp_local_write(self, file: UploadFile) -> str:
        try:
            file_ext = file.filename.split(".")[-1]
            path = f"{self.temp_dir}/{uuid4().hex}.{file_ext}"
            with open(path, "wb") as f:
                f.write(file.file.read())
            self.localpaths.append(path)
            return path
        except Exception as error:
            logger.error(f"failed during write temp file. {error=}")


class ExternalFileHandler(FileHandler):
    """
    """
    def __init__(self):
        super().__init__()

    def temp_download(self, url: str) -> str:
        """
        """
        try:
            # construct path
            file_ext = url.split(".")[-1]
            path = f"{self.temp_dir}/{uuid4().hex}.{file_ext}"
            self.localpaths.append(path)

            # download and write
            response = requests.get(url)
            with open(path, "wb") as file:
                file.write(response.content)

            return path
        except Exception as error:
            logger.error(f"failed during download temp file. {error=}")


def extract_document(filepath: str) -> str:
    """
    """
    try:
        document = docx.Document(filepath)
        return "\n".join([par.text for par in document.paragraphs])
    except Exception as error:
        logger.error(f"failed when extracting document. {filepath=} {error=}")
        raise error


def extract_external_document(url: str) -> str:
    """
    """
    try:
        with ExternalFileHandler() as handler:
            file_path = handler.temp_download(url)
            return extract_document(file_path)
    except Exception as error:
        logger.error(f"failed when extracting external document. {url=} {error=}")
        raise error
