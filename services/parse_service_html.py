import concurrent.futures
from lxml import html
from typing import Any
import re
from beanie import PydanticObjectId
from models.discrepancy import ValidatorCode
from multiprocessing import cpu_count
from services.parse_service_base import IParserDataService
from services.storage_file_reader_service import StorageFileReaderService
from resources.config import app_config, logger
from resources.exception import EmptyFileListError
from services.parse_logger_discrepancy import ParserDataLoggerDiscrepancyService, Discrepancy


class ParserDataServiceHTML(IParserDataService):
    @classmethod
    async def parse(cls, *, path: str, files: list[str], path_file_tests: str | None = None) -> list[dict[str, Any]]:
        if len(files) == 0:
            raise EmptyFileListError

        num_cores: int = cpu_count()  # Number of CPU cores (including logical cores)
        with concurrent.futures.ProcessPoolExecutor(num_cores):
            pages = await StorageFileReaderService.read_all(path=path, files=files)
            page_res: list[dict[str, Any]] = []
            index: int = 0  # For tracking file name from list, and adding this data to pages
            for page in pages:  # 1-N documets content in a list of string
                logger.info(f"start page {page} parsing - {cls.__name__}\r\n")
                tree = html.fromstring(page)
                page_dict: dict[str, Any] = {"file_name": files[index], "type": "html"}
                index += 1
                html_items = app_config.docs_rules["html"].items()  # Data extraction page rules

                item_discrepancy_details: str = ""

                for key, val in html_items:
                    if key != "schema_version":
                        if isinstance(val, dict):
                            attr: str = val.get("attr")
                            cmd: str = val.get("cmd")
                            regex: str = val.get("regex")
                            '''If one of the Parameters is None it might produced an error exception, 
                            depended on the implemented extraction behavior implemented in lax_parser'''
                            try:
                                scraper_val: list[dict[str, Any]] | dict[str, Any] | list[int]= await cls.lxml_parser(tree=tree, cmd=cmd, attr=attr,  regex=regex)
                                if len(scraper_val) == 0:
                                    scraper_val = {"value": "", "error": f"Missing item for {cmd}", "location": -1}
                            except Exception as e:
                                scraper_val = {"value": "", "error": f"Missing item for {cmd}", "location": -1}

                            page_dict[key] = scraper_val
                    else:
                        page_dict[key] = val

                logger.info(f"end page {page} parsing - {cls.__name__}\r\n")
                page_res.append(page_dict)
            return page_res

    @staticmethod
    async def lxml_parser(*, tree: Any, cmd: str, attr: str | None = None,
                          regex: dict[str, str] | None = None) -> list[str] | \
                                                                  list[int] | \
                                                                  dict[str, Any]:

        if attr is not None:
            element: Any = tree.xpath(cmd)[0]
            return {"value": element.attrib[attr], "location": element.sourceline}

        elements: Any = tree.xpath(cmd)
        if isinstance(elements, list) and len(elements) == 1:
            element: Any = elements[0]

            if regex is not None:
                dict_res: dict[str, Any] = {"value": element.text, "location": element.sourceline}
                for key, val in regex.items():
                    v_reg = re.findall(val, element.text)

                    if len(v_reg) == 1:
                        dict_res[key] = v_reg[0]
                    else:
                        dict_res[key] = ' '.join(v_reg)

                return dict_res

            return {"value": element.text, "location": element.sourceline}

        list_res: list[dict[str, Any]] = []
        row_no: int = 0
        col_no: int = 0
        for element in elements:
            if element.tag == "tr":
                dic_res: dict[str, Any] = {}
                # Keep previous dictionary of row and columns data into recurrent result list

                list_res.append(dic_res)
                col_no = 0
                dic_res[f'row'] = {"row": row_no, "location": element.sourceline}
                dic_res['columns'] = []

                logger.debug(f"Parsing document: start row={row_no}, "
                             f"location {element.sourceline}")
                row_no += 1
            else:
                dic_res['columns'].append({"col": col_no, "location": element.sourceline,
                                           "value": element.text})
                logger.debug(
                    f"Parsing document: column={col_no}, location {element.sourceline}, value={element.text}")
                col_no += 1

        return list_res
