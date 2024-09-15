from beanie import Document, Indexed
from pydantic import BaseModel
from typing import Optional
import uuid
import pytz
from datetime import datetime
from enum import IntEnum


class ValidatorCode(IntEnum):
    ERROR = 0,
    VALID = 2,
    IN_VALID = 3,
    NOT_PROCESSED = 4


class CompareDiscrepancy(BaseModel):  # pylint: disable=R0901
    _id: Optional[str] = None
    document_id: str
    file_name: str
    schema_version: str
    discrepancy_type: str
    validation: ValidatorCode = ValidatorCode.VALID


class Discrepancy(BaseModel):  # pylint: disable=R0901
    _id: str = str(uuid.uuid4())  # type: ignore
    document_id: str
    file_name: str
    discrepancy_type: str
    location: int
    details: str
    schema_version: str
    date_time: datetime = datetime.now(tz=pytz.utc)


class DiscrepancyDB(Document):  # pylint: disable=R0901
    _id: Indexed(str, unique=True)  # type: ignore
    document_id: Indexed(str)
    file_name: str
    discrepancy_type: str
    location: int
    details: str
    schema_version: Indexed(str)
    date_time: datetime

    class Settings:
        name = "discrepancy"
