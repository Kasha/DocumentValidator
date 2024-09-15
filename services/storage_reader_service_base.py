from abc import ABC, abstractmethod
from typing import Any


class IStorageReaderService(ABC):
    @classmethod
    @abstractmethod
    async def read(cls, *, file: str) -> str:
        pass

    @classmethod
    @abstractmethod
    async def read_all(cls, *, path: str, files: list[str]) -> list[str]:
        pass
