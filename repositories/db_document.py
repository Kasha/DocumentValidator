from pydantic import ValidationError
from repositories.db_base import ICollectionRepository, Model, Document, Any
from models.docs import DocsDB, Doc, CompareDoc
from resources.defines import logger
from resources.exception import ItemDBCreationError
from resources.config import app_config
from beanie.odm.operators.update.general import Set
from beanie import BulkWriter


class DocumentRepository(ICollectionRepository):
    async def create(self, data: Model) -> Document:
        """Create document in the database"""
        new_data: Document = DocsDB(**data.dict())

        logger.debug(
            f"Attempting to a create new document data in mongodb database, {DocsDB.Settings.name} collection. "
            f"document_id:{new_data.document_id['value']}, "
            f"file_name:{new_data.file_name}, "
            f"schema_version:{new_data.schema_version}, "
            f"type:{new_data.type}",
        )

        await new_data.insert()

        if not new_data.id:
            msg: str = f"failed creating document in mongodb, {DocsDB.Settings.name} collection for data: {new_data.dict()}"
            logger.debug(msg)
            return None
        logger.debug(
            f"successfully created document in mongodb database {DocsDB.Settings.name} collection"
        )
        return new_data

    async def read(self, data: Model) -> Document:
        item_doc_model: CompareDoc = CompareDoc(**data.dict())
        logger.debug(
            f"attempting to read document from {DocsDB.Settings.name} collection for document_id={item_doc_model.document_id}, "
            f"schema_version={item_doc_model.schema_version}, file_name={item_doc_model.file_name} file_type={item_doc_model.type}"
        )

        result = await DocsDB.find_one(
            DocsDB.document_id["value"] == item_doc_model.document_id,
            DocsDB.schema_version == item_doc_model.schema_version,
            DocsDB.file_name == item_doc_model.file_name,
            DocsDB.type == item_doc_model.type,
        )
        if result is None:
            logger.debug(
                f"failed reading document_id={item_doc_model.document_id},"
                f"schema_version={item_doc_model.schema_version}, "
                f"file_name={item_doc_model.file_name}"
                f" from mongodb database, {DocsDB.Settings.name} collection, document was not found"
            )
            return None

        logger.debug(
            f"successfully read document from mongodb database, {DocsDB.Settings.name} collection"
        )
        return result

    async def update(
            self, data: Model
    ) -> Any:
        """Update document in the database"""
        item_update_data_doc: Document = DocsDB(**data.dict())

        logger.debug(
            f"Attempting to a create or update document data in mongodb database, docs collection. "
            f"document_id:{item_update_data_doc.document_id['value']}, "
            f"file_name:{item_update_data_doc.file_name}, "
            f"schema_version:{item_update_data_doc.schema_version}, "
            f"type:{item_update_data_doc.type}",
        )

        item_updated = await DocsDB.find_one(DocsDB.document_id["value"] == item_update_data_doc.document_id["value"],
                                             DocsDB.schema_version == item_update_data_doc.schema_version,
                                             DocsDB.file_name == item_update_data_doc.file_name,
                                             DocsDB.type == item_update_data_doc.type,
                                             ).upsert(
            {
                "$set": {
                    **data.dict()
                }
            },
            on_insert=item_update_data_doc,
        )

        logger.debug(
            f"successfully updated document in mongodb database, {DocsDB.Settings.name} collection"
        )
        return item_updated

    async def update_many(self, documents: list[dict[str, Any]]) -> list[Any]:
        """Update many documents in the database, do an upsert and wrap with a transaction"""

        res_insert_or_update_docs: list[Any] = []
        async with await DocsDB.get_motor_collection().database.client.start_session() as session:
            async with session.start_transaction():
                for data in documents:
                    items_doc_model: Model = Doc(**data)
                    item_data_doc_db: Document = DocsDB(**items_doc_model.dict())

                    logger.debug(
                        f"Attempting to a create or update document data in mongodb database, docs collection. "
                        f"document_id:{item_data_doc_db.document_id['value']}, "
                        f"file_name:{item_data_doc_db.file_name}, "
                        f"schema_version:{item_data_doc_db.schema_version}, "
                        f"type:{item_data_doc_db.type}",
                    )

                    item_insert_or_update_doc = await DocsDB.find_one(
                        DocsDB.document_id["value"] == item_data_doc_db.document_id["value"],
                        DocsDB.schema_version == item_data_doc_db.schema_version,
                        DocsDB.file_name == item_data_doc_db.file_name,
                        DocsDB.type == item_data_doc_db.type
                    ).upsert(Set({
                        **items_doc_model.dict()
                    }), on_insert=item_data_doc_db, session=session)
                    if isinstance(item_insert_or_update_doc, DocsDB):
                        msg: str = f"File: {item_data_doc_db.file_name} was inserted successfully into {DocsDB.Settings.name} collection"
                    else:
                        msg: str = f"File: {item_data_doc_db.file_name} was updated successfully into {DocsDB.Settings.name} collection"
                    print(msg)
                    logger.debug(msg)
                    res_insert_or_update_docs.append(item_insert_or_update_doc)
            logger.info(
                f"successfully updated many document in mongodb database, {DocsDB.Settings.name} collection"
            )

        return res_insert_or_update_docs

    async def delete(self, data: Model) -> None:
        """delete document from the database"""
        item_doc_model: CompareDoc = CompareDoc(**data.dict())
        logger.debug(
            f"attempting to delete document from {DocsDB.Settings.name} collection for document_id={item_doc_model.document_id}, "
            f"schema_version={item_doc_model.schema_version}, file_name={item_doc_model.file_name} file_type={item_doc_model.type}"
        )
        item_doc: Document = await self.read(item_doc_model)

        if item_doc is None:
            return None

        await item_doc.delete()
        logger.debug(
            f"successfully deleted document from mongodb database, {DocsDB.Settings.name} collection"
        )
