# pylint: disable=E0213
"""Application configurations"""
import logging
from os import getenv
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel
from enum import Enum, IntEnum


class EnvTypes(str, Enum):
    """Possible environment"""
    PROD: str = "prod"
    STG: str = "stg"
    DEV: str = "dev"


load_dotenv()

env: str = getenv("STAGING", "dev").lower()


class AppSettings(BaseModel):
    """Shared settings to all"""
    ENV: EnvTypes = env
    LOGGING_LEVEL: int = logging.DEBUG
    ABS_DIR: str = f"{str(Path(__file__).parent.parent.resolve())}"
    CONFIG_DIR: str = f"{ABS_DIR}/resources/"
    CONFIG_DOCS_FILE_NAME: str = f"{CONFIG_DIR}docs_config.yaml"
    CONFIG_TESTS_FILE_NAME: str = f"{CONFIG_DIR}tests_config.yaml"
    DEFAULT_TEST_FILE: str = getenv("STORAGE_TEST_FILE_NAME", "discrepancy1.yaml")
    STORAGE_DIR: str = f"{str(Path(__file__).parent.parent.resolve())}/storage/"
    ABS_TEST_FILE_NAME: str = f"{STORAGE_DIR}{DEFAULT_TEST_FILE}"
    LOG_FILE_NAME: str = f'{env}_beancure_alert.log'
    DB_USER: str = getenv("DB_USER")
    DB_PASSWORD: str = getenv("DB_PASSWORD")
    DB_NAME: str = getenv("DB_NAME")


class AppProdSettings(AppSettings):
    """Production specific settings"""
    LOGGING_LEVEL: int = logging.INFO


class AppStgSettings(AppSettings):
    """Staging specific settings"""
    pass


class AppDevSettings(AppSettings):
    """Development specific settings"""
    pass


def _get_app_settings() -> AppSettings:
    """Factory method to choose settings according to environment"""
    match env:
        case EnvTypes.PROD:
            return AppProdSettings()  # pragma: no cover
        case EnvTypes.STG:
            return AppStgSettings()  # pragma: no cover

    return AppDevSettings()  # pragma: no cover


app_settings = _get_app_settings()
