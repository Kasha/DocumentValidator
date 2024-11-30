from repositories.db_base import ICollectionRepository, Model, Document, Any
from models.discrepancy import DiscrepancyDB, Discrepancy, CompareDiscrepancy
from resources.defines import logger
from resources.exception import ItemDBCreationError


class DiscrepancyRepository(ICollectionRepository):
    async def create(self, data: Model) -> Document:
        """Create the discrepancy in the database"""
        logger.debug(
            "attempting to create new discrepancy data in mongodb database",

        )
        new_data = DiscrepancyDB(**data.dict())  # type: ignore
        await new_data.insert()
        if not new_data.id:
            logger.debug(
                "failed creating in mongodb database"
            )
            raise ItemDBCreationError
        logger.debug(
            f"successfully created in mongodb database {new_data}, {DiscrepancyDB.Settings.name} collection",

        )
        return new_data

    async def read(self, data: Model) -> Document:
        item_model: CompareDiscrepancy = CompareDiscrepancy(**data.dict())
        logger.debug(
            f"attempting to read discrepancy from {DiscrepancyDB.Settings.name} collection for document_id={item_model.document_id}, "
            f"schema_version={item_model.schema_version}, file_name={item_model.file_name} discrepancy_type={item_model.discrepancy_type}"
        )
        res_doc: Document = None
        if item_model.id is not None:
            res_doc = await DiscrepancyDB.get(item_model.id)
        else:
            res_doc = await DiscrepancyDB.find_one(
                DiscrepancyDB.document_id == item_model.document_id,
                DiscrepancyDB.schema_version == item_model.schema_version,
                DiscrepancyDB.file_name == item_model.file_name,
                DiscrepancyDB.discrepancy_type == item_model.discrepancy_type,
            )
        if res_doc is None:
            logger.debug(
                f"failed reading discrepancy document_id={item_model.document_id},"
                f"schema_version={item_model.schema_version}, "
                f"file_name={item_model.file_name}, "
                f"discrepancy_type={item_model.discrepancy_type}"
                f" from mongodb database, {item_model.Settings.name} collection, document was not found"
            )
            return None

        logger.debug(
            f"successfully read discrepancy from mongodb database, {DiscrepancyDB.Settings.name} collection"
        )
        return res_doc

    async def update(
            self, data: Model
    ) -> Any:
        """Update document in the database"""
        item_update_data_doc: Document = DiscrepancyDB(**data.dict())

        logger.debug(
            f"Attempting to a create or update discrepancy data in mongodb database, docs collection. "
            f"document_id:{item_update_data_doc.document_id}, "
            f"file_name:{item_update_data_doc.file_name}, "
            f"schema_version:{item_update_data_doc.schema_version}, "
            f"discrepancy_type:{item_update_data_doc.discrepancy_type}",
        )
        if item_update_data_doc.id is not None:
            item_updated = await DiscrepancyDB.find_one(DiscrepancyDB.id == item_update_data_doc.id).upsert(
                {
                    "$set": {
                        **data.dict()
                    }
                },
                on_insert=item_update_data_doc,
            )
        else:
            item_updated = await DiscrepancyDB.find_one(DiscrepancyDB.document_id == item_update_data_doc.document_id,
                                                        DiscrepancyDB.schema_version == item_update_data_doc.schema_version,
                                                        DiscrepancyDB.file_name == item_update_data_doc.file_name,
                                                        DiscrepancyDB.discrepancy_type == item_update_data_doc.discrepancy_type,
                                                        ).upsert(
                {
                    "$set": {
                        **data.dict()
                    }
                },
                on_insert=item_update_data_doc,
            )
        logger.debug(
            f"successfully updated discrepancy in mongodb database, {DiscrepancyDB.Settings.name} collection"
        )
        return item_updated

    async def update_many(self, documents: list[dict[str, Any]]) -> list[Any]:
        pass

    async def delete(self, data: Model) -> None:
        """delete discrepancy from the database"""
        item_doc_model: CompareDiscrepancy = CompareDiscrepancy(**data.dict())
        logger.debug(
            f"attempting to read discrepancy from {DiscrepancyDB.Settings.name} collection for document_id={item_doc_model.document_id}, "
            f"schema_version={item_doc_model.schema_version}, file_name={item_doc_model.file_name} "
            f"discrepancy_type={item_doc_model.discrepancy_type}"
        )
        item_doc: Document = await self.read(item_doc_model)

        if item_doc is None:
            return None

        await item_doc.delete()
        logger.debug(
            f"successfully deleted discrepancy from mongodb database, {DiscrepancyDB.Settings.name} collection"
        )
