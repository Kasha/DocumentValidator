from domains.document_validator_domain_base import IDocumentValidator, Model, ValidatorCode
from clients.document_validator_client_base import IDocumentValidatorClient


class DocumentValidator(IDocumentValidator):
    def __new__(cls, *, validator_client: IDocumentValidatorClient):
        """ creates a singleton object, if it is not created,
        or else returns the previous singleton object"""
        if not hasattr(cls, 'instance'):
            cls.instance = super(DocumentValidator, cls).__new__(cls)
            cls.instance.validator_client = validator_client

        return cls.instance

    @classmethod
    async def validate_all(cls, *, file_type: str | None = None, schema_version: str | None = None,
                           path_file_tests: str | None = None) -> None:
        await cls.instance.validator_client.validate_all(file_type=file_type, schema_version=schema_version,
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
        return await cls.instance.validator_client.validate(file_type=file_type, schema_version=schema_version,
                                                            path_file_tests=path_file_tests)
