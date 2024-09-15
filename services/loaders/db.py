"""module for db loaders"""
import asyncio
import urllib.parse

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from resources.settings import AppSettings, app_settings
from models.discrepancy import Discrepancy, DiscrepancyDB
from models.docs import DocsDB


async def load_db() -> AsyncIOMotorClient:
    db_username = urllib.parse.quote(app_settings.DB_USER)  # pragma: no cover
    db_password = urllib.parse.quote(app_settings.DB_PASSWORD)  # pragma: no cover
    mongo_uri = f"mongodb+srv://{db_username}:{db_password}" \
                f"@cluster0.ugnka.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

    client = AsyncIOMotorClient(mongo_uri)
    client.admin.command('ping')
    client.get_io_loop = asyncio.get_event_loop

    await init_beanie(
        database=client[app_settings.DB_NAME],
        document_models=[
            DiscrepancyDB,
            DocsDB
        ]
    )

    return client
