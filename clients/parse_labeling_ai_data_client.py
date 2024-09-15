from clients.parse_data_client_base import IParserDataClient


class ParserLabelingAIDataClient(IParserDataClient):
    """Empty class for future Labeling parsed data"""
    @classmethod
    async def parse(cls, *, path_file: str, path_file_tests: str | None = None) -> None:
        pass
