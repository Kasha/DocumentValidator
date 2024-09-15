import pytz
from datetime import datetime
from services.parse_logger_base import IParserDataLoggerService, Model
from repositories.db_discrepancy import DiscrepancyRepository, Discrepancy
from resources.defines import logger


class ParserDataLoggerDiscrepancyService(IParserDataLoggerService):
    @classmethod
    async def parse_logger(cls, *, data: Model) -> None:
        if isinstance(data, Discrepancy):
            doc: Discrepancy = Discrepancy(**data.dict())
            logger.info(
                f"Error parsing document - {doc}")
            print(
                f"Error parsing document Invalid document - {doc}")

        await DiscrepancyRepository().update(data)

    @classmethod
    async def validation_logger(cls, *, data: Model) -> None:
        if isinstance(data, Discrepancy):
            doc: Discrepancy = Discrepancy(**data.dict())
            logger.info(f"{doc.validate} document - {doc}")
            print(f"{doc.validate} document - {doc}")
            await DiscrepancyRepository().update(data)
