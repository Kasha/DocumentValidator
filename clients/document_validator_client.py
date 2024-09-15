from beanie import Document
from clients.document_validator_client_base import (
    IDocumentValidatorClient,
    ValidatorCode, Model)
from services.validator_service_base import IDocumentValidatorService
from models.discrepancy import Discrepancy
from repositories.db_base import ICollectionRepository


class DocumentValidatorClient(IDocumentValidatorClient):
    def __new__(cls, *, validator_service: IDocumentValidatorService, repository_service: ICollectionRepository):
        """ creates a singleton object, if it is not created,
        or else returns the previous singleton object"""
        if not hasattr(cls, 'instance'):
            cls.instance = super(DocumentValidatorClient, cls).__new__(cls)
            cls.instance.validator_service = validator_service
            cls.instance.repository_service = repository_service

        return cls.instance

    @classmethod
    async def validate_all(cls, *, file_type: str | None = None, schema_version: str | None = None,
                           path_file_tests: str | None = None) -> None:
        await cls.instance.validator_service.validate_all(file_type=file_type,
                                                          schema_version=schema_version,
                                                          path_file_tests=path_file_tests)

    @classmethod
    async def validate(cls, *, file_type: str | None = None, schema_version: str | None = None,
                       path_file_tests: str | None = None) -> (ValidatorCode, Model):
        """
                Parameters:
                    file_type: Search filter - file type to search and validate, default = None (All)
                    schema_version: Search filter - Parsing defined schema_version
                    for rules input file/config that was used to parse documents.
                    path_file_tests: path or file for validating data

                Returns:
                     ValidatorCode enum:
                        ERROR = 0,
                        VALID = 2,
                        IN_VALID = 3,
                        NOT_PROCESSED = 4

                        and discrepancy model describing validation result
                            """

        return await cls.instance.validator_service.validate("long_title", 50)
