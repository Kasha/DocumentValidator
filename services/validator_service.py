from services.validator_service_base import \
    (IDocumentValidatorService, ValidatorCode, Model, datetime, Union)
from beanie import Document
from resources.config import app_config
from models.discrepancy import Discrepancy
from models.docs import DocsDB, Doc, CompareDoc, Any
from services.parse_logger_discrepancy import ParserDataLoggerDiscrepancyService


class DocumentValidatorService(IDocumentValidatorService):
    @classmethod
    async def find_short_titles(cls, max_length: int) -> None:
        pipeline = [
            {
                "$addFields": {
                    "titleLength": {"$strLenCP": "$title.value"}
                }
            },
            {
                "$match": {
                    "titleLength": {"$lt": max_length}
                }
            }
        ]
        async for doc in DocsDB.aggregate(pipeline):
            dic_disc: dict[str, Any] = {"document_id": doc["document_id"]["value"],
                                        "file_name": doc["file_name"],
                                        "discrepancy_type": "short title",
                                        "location": doc["title"]["location"],
                                        "details": f"title: {doc['title']['value']}, reaseon: Shorter than:{max_length}",
                                        "schema_version": doc["schema_version"]}
            discrepancy_details_model = Discrepancy(**dic_disc)
            # print(discrepancy_details_model)
            await ParserDataLoggerDiscrepancyService.validation_logger(data=discrepancy_details_model)

    @classmethod
    async def find_long_titles(cls, max_length: int) -> None:
        pipeline = [
            {
                "$addFields": {
                    "titleLength": {"$strLenCP": "$title.value"}
                }
            },
            {
                "$match": {
                    "titleLength": {"$gt": max_length}
                }
            }
        ]
        async for doc in DocsDB.aggregate(pipeline):
            dic_disc: dict[str, Any] = {"document_id": doc["document_id"]["value"],
                                        "file_name": doc["file_name"],
                                        "discrepancy_type": "long title",
                                        "location": doc["title"]["location"],
                                        "details": f"title: {doc['title']['value']}, reaseon: Longer than:{max_length}",
                                        "schema_version": doc["schema_version"],
                                        "validation": ValidatorCode.IN_VALID}
            discrepancy_details_model = Discrepancy(**dic_disc)
            # print(discrepancy_details_model)
            await ParserDataLoggerDiscrepancyService.validation_logger(data=discrepancy_details_model)

    @classmethod
    async def find_short_title(cls, max_length: int) -> Model:
        pipeline = [
            {
                "$addFields": {
                    "titleLength": {"$strLenCP": "$title.value"}
                }
            },
            {
                "$match": {
                    "titleLength": {"$lt": max_length}
                }
            }
        ]
        async for doc in DocsDB.aggregate(pipeline):
            dic_disc: dict[str, Any] = {"document_id": doc["document_id"]["value"],
                                        "file_name": doc["file_name"],
                                        "discrepancy_type": "short title",
                                        "location": doc["title"]["location"],
                                        "details": f"title: {doc['title']['value']}, reaseon: Shorter than:{max_length}",
                                        "schema_version": doc["schema_version"]}
            discrepancy_details_model = Discrepancy(**dic_disc)
            # print(discrepancy_details_model)
            await ParserDataLoggerDiscrepancyService.validation_logger(data=discrepancy_details_model)
            return discrepancy_details_model

    @classmethod
    async def find_long_title(cls, max_length: int) -> Model:
        pipeline = [
            {
                "$addFields": {
                    "titleLength": {"$strLenCP": "$title.value"}
                }
            },
            {
                "$match": {
                    "titleLength": {"$gt": max_length}
                }
            }
        ]
        async for doc in DocsDB.aggregate(pipeline):
            dic_disc: dict[str, Any] = {"document_id": doc["document_id"]["value"],
                                        "file_name": doc["file_name"],
                                        "discrepancy_type": "long title",
                                        "location": doc["title"]["location"],
                                        "details": f"title: {doc['title']['value']}, reaseon: Longer than:{max_length}",
                                        "schema_version": doc["schema_version"],
                                        "validation": ValidatorCode.IN_VALID}
            discrepancy_details_model = Discrepancy(**dic_disc)
            # print(discrepancy_details_model)
            await ParserDataLoggerDiscrepancyService.validation_logger(data=discrepancy_details_model)
            return discrepancy_details_model

    @classmethod
    async def validate_all(cls, *, file_type: str | None = None, schema_version: str | None = None,
                           path_file_tests: str | None = None) -> None:
        await cls.find_long_titles(60)
        await cls.find_short_titles(10)

    @classmethod
    async def validate(cls, *, test_name: str, val: Union[int, datetime], doc: Document) -> (ValidatorCode, Model):
        doc: Discrepancy = None
        if test_name == "long_title":
           doc: Discrepancy = await cls.find_long_title(val)

        return tuple(ValidatorCode.VALID, doc)
