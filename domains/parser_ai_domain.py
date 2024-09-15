from domains.parser_domain_base import IParser
from clients.parse_labeling_ai_data_client import ParserLabelingAIDataClient


class Parser(IParser):
    @classmethod
    async def parse(cls, *, path_file: str, path_file_tests: str | None = None) -> None:
        """
        Description: detects structure and validity rules
        Parameters:
            path_file: path or file for parsing data,
            path_file_tests: path or file for testing data

        Returns:
             None
        """
        await ParserLabelingAIDataClient.parse(path_file=path_file, path_file_tests=path_file_tests)