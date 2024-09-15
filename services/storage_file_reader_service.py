import asyncio
import aiofiles
from typing import Any
from services.storage_reader_service_base import IStorageReaderService


class StorageFileReaderService(IStorageReaderService):
    @classmethod
    async def read(cls, *, file: str) -> str:
        """ Asynchronously reading a single file """
        async with aiofiles.open(file, 'r') as f:
            return await f.read()

    @classmethod
    async def read_all(cls, *, path: str, files: list[str]) -> list[str]:
        tasks = [cls.read(file=f"{path}{file}") for file in files]
        return await asyncio.gather(*tasks)
