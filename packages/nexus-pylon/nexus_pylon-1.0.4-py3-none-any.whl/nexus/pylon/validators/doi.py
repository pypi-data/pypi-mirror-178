import hashlib
from io import BytesIO
from typing import Optional

from nexus.pylon.exceptions import BadResponseError
from nexus.pylon.pdftools import is_pdf
from nexus.pylon.validators.base import BaseValidator
import PyPDF2
from PyPDF2.errors import PdfReadError


class PdfValidator(BaseValidator):
    def __init__(self, doi: str, md5: Optional[str] = None):
        self.doi = doi
        self.md5 = md5
        self.file = bytes()
        self.v = hashlib.md5()

    def update(self, chunk):
        self.file += chunk
        if self.md5:
            self.v.update(chunk)

    def validate(self):
        if self.md5 and self.md5.lower() == self.v.hexdigest().lower():
            return
        elif not is_pdf(f=self.file):
            raise BadResponseError(doi=self.doi, file=str(self.file[:100]))

        try:
            PyPDF2.PdfReader(BytesIO(self.file))
        except PdfReadError:
            raise BadResponseError(doi=self.doi, file=str(self.file[:100]))
