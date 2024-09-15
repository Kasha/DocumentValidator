from typing import Any
import importlib
from typing import Any
from services.parse_service_html import ParserDataServiceHTML
from services.parse_service_pdf import ParserDataServicePDF


def class_factory_by_module(*, module_name: str, class_name: str) -> Any:
    """ Class Factory Like (Dynamic class instantiation by module and name)"""
    module = importlib.import_module(module_name)
    class_ = getattr(module, class_name, None)
    return class_() if class_ is not None else None


def class_factory(*, class_name: str) -> Any:
    """ Class Factory Like (Dynamic class instantiation by name, requires a static class import)"""

    name: str = f'{class_name}'
    # No need for object  instance, but class reference for static service call
    return globals()[name]
