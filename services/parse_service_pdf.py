from services.parse_service_base import IParserDataService, Any
from resources.exception import ParserServiceNotImplementedError


class ParserDataServicePDF(IParserDataService):
    @classmethod
    async def parse(cls, *, path: str, files: list[str], path_file_tests: str | None = None) -> list[dict[str, Any]]:
        raise ParserServiceNotImplementedError(f"{ParserServiceNotImplementedError.details} for {cls.__name__}")
