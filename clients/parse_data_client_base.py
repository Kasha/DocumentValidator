from abc import ABC, abstractmethod


class IParserDataClient(ABC):
    @classmethod
    @abstractmethod
    async def parse(cls, *, path_file: str, path_file_tests: str | None = None) -> None:
        pass
