from abc import ABC, abstractmethod
from beanie import Document
from typing import Any
from domains.document_validator_domain_base import ValidatorCode, Model
import datetime
from typing import Union

class IDocumentValidatorService(ABC):
    @classmethod
    @abstractmethod
    async def validate_all(cls, *, file_type: str | None = None, schema_version: str | None = None,
                           path_file_tests: str | None = None) -> None:
        pass

    @classmethod
    @abstractmethod
    async def validate(cls, *, test_name: str, val: Union[int, datetime],  doc: Document) -> (ValidatorCode, Model):
        pass
