from domains.parser_domain_base import IParser
from clients.parse_data_client_base import IParserDataClient


class Parser(IParser):
    def __new__(cls, *, parser_client: IParserDataClient):
        """ creates a singleton object, if it is not created,
        or else returns the previous singleton object"""
        if not hasattr(cls, 'instance'):
            cls.instance = super(Parser, cls).__new__(cls)
            cls.instance.paser_client = parser_client

        return cls.instance

    @classmethod
    async def parse(cls, *, path_file: str, path_file_tests: str | None = None) -> None:
        """
        Parameters:
            path_file: path or file for parsing data,
            path_file_tests: path or file for testing data

        Returns:
             None
        """
        await cls.instance.paser_client.parse(path_file=path_file, path_file_tests=path_file_tests)
