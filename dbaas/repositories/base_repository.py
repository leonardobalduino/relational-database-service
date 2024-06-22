import copy
import typing

from bson import ObjectId
from pymongo import ReturnDocument
from pymongo.collection import Collection

from dbaas.configs.mongo import database
from dbaas.models.base_model import BaseModel
from dbaas.utils.utils import utcnow

if typing.TYPE_CHECKING:
    from pymongo.results import DeleteResult, InsertOneResult

E = typing.TypeVar("E", bound=BaseModel)


class BaseRepository(typing.Generic[E]):
    def __init__(self, entity: typing.Type[E]):
        self._collection = entity.__name__.lower()
        self._entity = entity

    def _fill_audit(self, dict_entity: dict, create: bool = False):
        now = utcnow()

        audit_info = {"updated_at": now}
        if create:
            audit_info["created_at"] = now

        return {**dict_entity, **audit_info}

    def _set_document_id(self, dict_entity: dict):
        is_object_id = isinstance(dict_entity.get("_id", None), ObjectId)
        field_pop, field_add = ("_id", "id") if is_object_id else ("id", "_id")

        if document_id := dict_entity.pop(field_pop, None):
            dict_entity[field_add] = ObjectId(document_id) if "_" in field_add else str(document_id)

        return dict_entity

    def _db_to_object(self, item: dict) -> E:
        dict_entity = copy.deepcopy(item)
        dict_entity = self._set_document_id(dict_entity)
        return self._entity(**dict_entity)

    def collection(self) -> Collection:
        return database[self._collection]

    async def get_by_id(self, id: str) -> E | None:
        item = await self.collection().find_one({"_id": ObjectId(id)})
        return self._db_to_object(item) if item else None

    async def find_by_filter(self, filter: dict) -> list[E]:
        result = self.collection().find(filter=filter)
        return [self._db_to_object(item) async for item in result]

    async def find_all(self) -> list[E]:
        result = self.collection().find()
        return [self._db_to_object(item) async for item in result]

    async def create(self, entity: E) -> E:
        mongo_dict = self._fill_audit(self._set_document_id(entity.model_dump()), True)
        insert_result: "InsertOneResult" = await self.collection().insert_one(mongo_dict)
        document_id = insert_result.inserted_id
        inserted_document = {"_id": document_id, **mongo_dict}
        entity = self._db_to_object(inserted_document)
        return entity

    async def update(self, entity: E) -> E | None:
        dict_entity = entity.model_dump()
        dict_entity = self._fill_audit(dict_entity)
        dict_entity = self._set_document_id(dict_entity)

        updated = await self.collection().find_one_and_update(
            {"_id": dict_entity["_id"]}, {"$set": dict_entity}, return_document=ReturnDocument.AFTER
        )
        if updated:
            updated_result = self._db_to_object(updated)
            return updated_result

        return None

    async def delete_by_id(self, id: str) -> bool:
        result_deleted: "DeleteResult" = await self.collection().delete_one({"_id": ObjectId(id)})
        return result_deleted.deleted_count > 0
