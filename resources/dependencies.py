from repositories.db_document import DocumentRepository
from clients.parse_data_client import ParserDataClient
from clients.document_validator_client import IDocumentValidatorClient, DocumentValidatorClient
from services.validator_service import DocumentValidatorService
from domains.document_validator_domain import DocumentValidator
from domains.parser_domain import Parser, IParser
from repositories.db_discrepancy import DiscrepancyRepository


def get_parser_domain() -> IParser:
    return Parser(parser_client=ParserDataClient(db_document_repository=DocumentRepository()))


def get_validator_domain() -> IDocumentValidatorClient:
    return DocumentValidator(validator_client=DocumentValidatorClient(
                                    validator_service=DocumentValidatorService(),
                                    repository_service=DiscrepancyRepository()))
