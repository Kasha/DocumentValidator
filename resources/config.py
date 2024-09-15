"""! @brief Defines the dynamic configuration class built from config.yaml."""
# @file config.py
#  - Configuration module.
#  - Creating Configuration singleton with Sensors new attributes taken from config.yaml
#
# @section author_configuration Author(s)
# - Created by Liad Kashanovsky on 29/04/2024.
#
# Copyright (c) 2024 Liad Kashanovsky.  All rights reserved.

from os import path

import yaml
from resources.exception import RuntimeFailedToReadConfigFileError
from typing import Any
from resources.defines import logger, app_settings


class Configuration(object):
    def __new__(cls):
        """ creates a singleton object, if it is not created,
        or else returns the previous singleton object"""
        if not hasattr(cls, 'instance'):
            cls.instance = super(Configuration, cls).__new__(cls)
            cls.docs_rules = cls.read_file(file_name=app_settings.CONFIG_DOCS_FILE_NAME)
            cls.tests_rules = cls.read_file(file_name=app_settings.CONFIG_TESTS_FILE_NAME)

        return cls.instance

    def __setattr__(self, name, value):
        raise RuntimeFailedToReadConfigFileError(details=f"Failed to set {name}={value}")

    @classmethod
    def read_file(cls, *, file_name: str, conf_rules_default: dict[str, Any] = None) -> dict[str, Any]:
        try:
            with open(file_name, 'r') as configFile:
                return yaml.safe_load(configFile)
        except FileNotFoundError as e:
            if conf_rules_default is None:
                cls.__log(f"Configuration - File Not Found: {file_name} Error:{e}.")
        except AttributeError as e:
            if conf_rules_default is None:
                cls.__log(f"Configuration "
                          f"- Attribute Error:{e}.")
        except (yaml.YAMLError, yaml.MarkedYAMLError) as e:
            cls.__log(f"Configuration "
                      f"- Yaml Attribute Error:{e}.")
        logger.info(f"Config couldn't open {file_name}. Using  default sets {conf_default}")
        return conf_rules_default

    @staticmethod
    def __log(message: str = "") -> None:
        print(message)
        logger.debug(message)
        raise RuntimeFailedToReadConfigFileError(details=message)


app_config = Configuration()
