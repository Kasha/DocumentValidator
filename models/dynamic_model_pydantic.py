from dyntamic.factory import DyntamicFactory, Model
from models.dynamic_model_base import IDynamicModel, Any
import json
from models.html_doc_json_scheme_model import html_doc_schema


class DynamicPydanticModel(IDynamicModel):
    def __init__(self):
        self.dmodel = None

    def create(self, *, schema: json) -> Model:
        factory = DyntamicFactory(schema,
                                  ref_template="#defs")  # here I use a custom ref_template to point to nested schemas
        self.dmodel = factory.make()  # here we get an actual pydantic model
        return self.dmodel

    def validate(self, *, data: json) -> bool:
        validated_model = self.dmodel.model_validate(data)  # usual validation by a pydantic model
