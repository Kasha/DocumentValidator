from beanie import Document, Indexed
from pydantic import BaseModel
from typing import Any
import pytz
from datetime import datetime


class CompareDoc(BaseModel):  # pylint: disable=R0901
    document_id: str
    file_name: str
    schema_version: str
    type: str


class Doc(BaseModel):  # pylint: disable=R0901
    document_id: dict[str, Any]
    file_name: str
    title: dict[str, Any]
    header: list[dict[str, Any]]
    body: list[dict[str, Any]]
    footer: dict[str, Any]
    schema_version: str
    type: str
    date_time: datetime = datetime.now(tz=pytz.utc)


class DocsDB(Document):  # pylint: disable=R0901
    document_id: Indexed(dict[str, Any])
    file_name: Indexed(str)
    title: dict[str, Any]
    header: list[dict[str, Any]]
    body: list[dict[str, Any]]
    footer: dict[str, Any]
    schema_version: Indexed(str)
    type: str
    date_time: datetime

    class Settings:
        name = "docs"
