from os import path, listdir
from pathlib import Path
import json
from clients.parse_data_client_base import IParserDataClient
from resources.config import app_config, logger
from resources.exception import InvalidInputPathError, Any
from resources.utils import class_factory
from repositories.db_discrepancy import DiscrepancyRepository, Discrepancy
from repositories.db_document import ICollectionRepository


class ParserDataClient(IParserDataClient):
    db_document_repository: ICollectionRepository = None

    def __new__(cls, *, db_document_repository: ICollectionRepository):
        """ creates a singleton object, if it is not created,
        or else returns the previous singleton object"""
        if not hasattr(cls, 'instance'):
            cls.instance = super(ParserDataClient, cls).__new__(cls)
            cls.db_document_repository = db_document_repository
        return cls.instance

    @classmethod
    async def parse(cls, *, path_file: str, path_file_tests: str | None = None) -> None:
        """
               Description:
                 Check if configured extension contains parser class and that there are 1 or more files to parse
                 If both cases are True concreate suitable service parser using FactoryClass
               Parameters:
                   path_file: path or file for parsing data,
                   path_file_tests: path or file for testing data

               Returns:
                    None
               """
        service_base_name: str = f"{cls.__name__.split('Client')[0]}Service"

        logger.info(f"Start Parsing {path_file} from {cls.__name__}")
        if path.exists(path_file):
            postfix_name: str = Path(path_file).suffix
            if postfix_name:
                postfix_name = postfix_name.lstrip(".")
                name: str = f'{service_base_name}{postfix_name.upper()}'
                module_name: str = f"services.parse_service_{postfix_name.lower()}"
                """ Class Factory Like (Dynamic class instantiation by module and name) 
                                    according to supported input file type. None if service for this type of input files
                                     is not supported"""
                service_obj = class_factory(class_name=name)
                if service_obj is not None:
                    """When path_file= one file with absolute path"""
                    await service_obj.parse(path="", files=[path_file])
                    logger.info(f"Finished Parsing {path_file} from {cls.__name__}")
            else:
                for key in app_config.docs_rules.keys():
                    name: str = f'{service_base_name}{key.upper()}'
                    module_name: str = f"services.parse_service_{key.lower()}"
                    """ Class Factory Like (Dynamic class instantiation by class name) 
                        according to supported input file type. None if service for this type of input files
                        is not supported"""
                    service_obj = class_factory(class_name=name)
                    if service_obj is not None:
                        files_list: list[str] = [i[0:] for i in listdir(path_file) if i.endswith(key)]
                        parsed_documents: list[dict[str, Any]] = await service_obj.parse(path=path_file,
                                                                                         files=files_list)

                        """Insert Parsed Documents into DB"""
                        await cls.db_document_repository.update_many(parsed_documents)

                        logger.info(f"Finished Parsing {path_file} from {cls.__name__}")
        else:
            raise InvalidInputPathError(details=f"Failed Parsing {path_file} from {cls.__name__}")
