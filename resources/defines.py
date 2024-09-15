import logging
from typing import Any
from resources.settings import app_settings


logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                    filename=app_settings.LOG_FILE_NAME, encoding='utf-8',
                    level=app_settings.LOGGING_LEVEL, datefmt='%Y-%m-%d %H:%M:%S')
