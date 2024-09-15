"""ABC for Attempts Repository"""
from abc import ABC, abstractmethod

from beanie import Document
from beanie import PydanticObjectId
from dyntamic.factory import Model
from typing import Any


class ICollectionRepository(ABC):
    @abstractmethod
    async def create(self, data: Model) -> Document:
        pass

    @abstractmethod
    async def read(self, data: Model) -> Document:
        pass

    @abstractmethod
    async def update(
            self, data: Model
    ) -> Any:
        pass

    @abstractmethod
    async def update_many(self, documents: list[dict[str, Any]]) -> list[Any]:
        pass

    @abstractmethod
    async def delete(self, data: Model) -> None:
        pass
