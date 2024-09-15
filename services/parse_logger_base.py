from abc import ABC, abstractmethod
from dyntamic.factory import Model


class IParserDataLoggerService(ABC):
    @classmethod
    @abstractmethod
    async def parse_logger(cls, *, data: Model) -> None:
        pass

    @classmethod
    @abstractmethod
    async def validation_logger(cls, *, data: Model) -> None:
        pass
