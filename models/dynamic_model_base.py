from abc import ABC, abstractmethod
import json
from typing import Any
from dyntamic.factory import DyntamicFactory, Model


class IDynamicModel(ABC):
    @abstractmethod
    async def create(self, *, schema: json) -> Model:
        pass

    @abstractmethod
    async def validate(self, *, data: json) -> bool:
        pass
