from abc import ABC, abstractmethod
from typing import Any


class IParserDataService(ABC):
    @classmethod
    @abstractmethod
    async def parse(cls, *, path: str, files: list[str], path_file_tests: str | None = None) -> list[dict[str, Any]]:
        pass
