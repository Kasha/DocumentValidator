from abc import ABC, abstractmethod
from typing import Any
from enum import IntEnum


class ErrorCode(IntEnum):
    INTERNAL_SERVER = 0,
    STORAGE_NOT_FOUND = 2,
    TEST_FILE_NOT_FOUND = 3,
    FAILED_TO_GENERATE_OUTPUT = 4,
    INVALID_OR_CORRUPT_INPUT_PATH = 5,
    INVALID_OR_CORRUPT_INPUT_FILE = 6,
    INVALID_OR_CORRUPT_TEST_PATH = 7,
    INVALID_OR_CORRUPT_TEST_FILE = 8,
    INVALID_ARGUMENTS = 9,
    MISMATCH_BETWEEN_DOC_AND_PARSED_RULES = 10,
    MISMATCH_BETWEEN_TEST_AND_PARSED_RULES = 11,
    RUNTIME_FAILED_TO_OPEN_CONFIG_FILE = 12,
    RUNTIME_EMPTY_VALUES_IN_CONFIG = 13,
    PARSER_SERVICE_NOT_IMPLEMENTED = 14,
    ITEM_DB_CREATION_ERROR = 15,
    EMPTY_FILE_LIST_ERROR = 16


class ClientErrorBase(ABC, Exception):
    def __init__(
            self,
            details: str | None = None,
    ):
        if not details:
            self.details = details

    @property
    @abstractmethod
    def error_code(self) -> int:
        pass

    @property
    @abstractmethod
    def details(self) -> str:
        pass

    def dictionary(self) -> dict[str, Any]:
        return {
            "error_code": self.error_code,
            "details": self.details,
            "extra": self.extra,
        }

    @classmethod
    def dict(cls) -> dict[str, Any]:
        return cls().dictionary()


class InternalServerError(ClientErrorBase):
    error_code: int = ErrorCode.INTERNAL_SERVER
    details: str = "Internal Server Error"


class StorageNotFoundError(ClientErrorBase):
    error_code: int = ErrorCode.STORAGE_NOT_FOUND
    details: str = "Storage Not Found"


class TestFileNotFoundError(ClientErrorBase):
    error_code: int = ErrorCode.TEST_FILE_NOT_FOUND
    details: str = "Test File Not Found"


class FailedToGenerateOutput(ClientErrorBase):
    error_code: int = ErrorCode.FAILED_TO_GENERATE_OUTPUT
    details: str = "Failed To Generate Output"


class InvalidInputPathError(ClientErrorBase):
    error_code: int = ErrorCode.INVALID_OR_CORRUPT_INPUT_PATH
    details: str = "Failed To Open Input Path"


class InvalidInputFileError(ClientErrorBase):
    error_code: int = ErrorCode.INVALID_OR_CORRUPT_INPUT_FILE
    details: str = "Failed To Open Input file"


class InvalidTestPathError(ClientErrorBase):
    error_code: int = ErrorCode.INVALID_OR_CORRUPT_TEST_PATH
    details: str = "Failed To Open Test Path"


class InvalidTestFileError(ClientErrorBase):
    error_code: int = ErrorCode.INVALID_OR_CORRUPT_TEST_FILE
    details: str = "Failed To Open Test File"


class InvalidArgumentsError(ClientErrorBase):
    error_code: int = ErrorCode.INVALID_ARGUMENTS
    details: str = "Invalid Arguments (valid docs or tests (or both ) should be sent"


class MismatchDocParsingRulesError(ClientErrorBase):
    error_code: int = ErrorCode.MISMATCH_BETWEEN_DOC_AND_PARSED_RULES
    details: str = "Invalid Document Type Parsing Rules"


class MismatchTestParsingRules(ClientErrorBase):
    error_code: int = ErrorCode.MISMATCH_BETWEEN_TEST_AND_PARSED_RULES
    details: str = "Invalid Document Type Test Parsing Rules"


class RuntimeFailedToReadConfigFileError(ClientErrorBase):
    error_code: int = ErrorCode.RUNTIME_FAILED_TO_OPEN_CONFIG_FILE
    details: str = "Failed To Read Config File, Runtime Error"


class RuntimeInvalidConfigFileError(ClientErrorBase):
    error_code: int = ErrorCode.RUNTIME_EMPTY_VALUES_IN_CONFIG
    details: str = "Failed To Read Analytic Values from Config, Runtime Error"


class ParserServiceNotImplementedError(ClientErrorBase):
    error_code: int = ErrorCode.PARSER_SERVICE_NOT_IMPLEMENTED
    details: str = "Parser Service wasn't implemented"


class ItemDBCreationError(ClientErrorBase):
    error_code: int = ErrorCode.ITEM_DB_CREATION_ERROR
    details: str = "Failed create item in DB"


class EmptyFileListError(ClientErrorBase):
    error_code: int = ErrorCode.EMPTY_FILE_LIST_ERROR
    details: str = "Empty list of Document to parse"
