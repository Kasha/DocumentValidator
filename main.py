import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from argparse import ArgumentParser
from services.loaders.db import load_db
from resources.defines import (
    app_settings,
    logger)

from resources.exception import (InvalidInputPathError,
                                 InvalidInputFileError,
                                 InvalidTestPathError,
                                 InvalidTestFileError,
                                 InvalidArgumentsError)

from domains.parser_domain_base import IParser
from domains.document_validator_domain_base import IDocumentValidator
from resources.dependencies import get_parser_domain, get_validator_domain


class CustomArgumentParser(ArgumentParser):
    def error(self, message):
        self.print_help()
        self.exit(1, f'\nError: {message}\n')


def parse_args() -> ArgumentParser:
    parser: ArgumentParser = ArgumentParser(description="For valid docs path or file - Execute: Parsing and Storing"
                                                        "\r\nFor valid tests path or file - "
                                                        "Execute: Validating stored documents with supplied tests"
                                                        "\r\nchecking if discrepancies=None"
                                                        "\r\nelse storing discrepancies"
                                                        "\r\n(search for discrepancies in input files)")
    parser.add_argument("--docs", help="*Required if tests is None."
                                       "\r\nAbsolute path - optional [file name]."
                                       "\r\nExecute: Parsing and Storing.")
    parser.add_argument("--tests", help="*Required if docs is None. "
                                        "\r\nAbsolute path - optional [file name] of yaml defined tests."
                                        "\r\nyaml file structure: "
                                        "\r\n{"
                                        "\r\ntest_set_name, "
                                        "[\r\n{test_type = 'query'}\r\n]"
                                        "\r\n}."
                                        "\r\nExecute: Validating stored documents with supplied tests"
                                        "\r\nchecking if discrepancies=None"
                                        "\r\nelse storing discrepancies"
                                        "\r\n(search for discrepancies in input files)")
    args = parser.parse_args()

    if not args.docs and not args.tests:
        logger.error("docs or tests should be defined and valid")
        raise InvalidArgumentsError
    if args.docs:
        logger.info(f"Execute: Parsing and Storing for "
                    f"f{args.docs}")
    if args.tests:
        logger.info(f"\r\nExecute: Validating stored documents {args.tests} tests"
                    "\r\nchecking if discrepancies=None"
                    "\r\nelse storing discrepancies"
                    "\r\n(search for discrepancies in input files)")

    return args


async def main() -> None:
    args: ArgumentParser = parse_args()
    db_client: AsyncIOMotorClient = None
    try:
        ################
        start_message: str = "Start - Parsing Document according to document set of rules"
        logger.info(start_message)
        print(start_message)
        # Connect and init MongoDB with MotorClient and beanie for Async operations using Pydentic Models
        db_client = await load_db()
        domain_parser: IParser = get_parser_domain()
        await domain_parser.parse(path_file=args.docs, path_file_tests=args.tests)
        end_message: str = f"Finsh - Parsing"
        logger.info(end_message)
        print(end_message)
        #################
        start_message: str = "Start - Validating Document according to document type and set ot test rules"
        logger.info(start_message)
        print(start_message)
        domain_document_validator: IDocumentValidator = get_validator_domain()
        print(await domain_document_validator.validate_all())
        #################
        end_message: str = f"Finsh - Validation"
        logger.info(end_message)
        print(end_message)
        ###################
    except (
            asyncio.TimeoutError,
            InvalidInputPathError,
            InvalidInputFileError,
            InvalidTestPathError,
            InvalidTestFileError,
            InvalidArgumentsError,
            ValueError,
            UnicodeDecodeError,
            IOError,
            Exception,
    ) as e:
        logger.error(e)
        print(e)
    finally:
        if db_client is not None:
            db_client.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    asyncio.run(main())
