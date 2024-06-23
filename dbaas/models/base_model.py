from datetime import datetime

import pydantic
from bson.objectid import ObjectId
from pydantic import ConfigDict, Field

from dbaas.utils.utils import encode_datetime, encode_object_id


class BaseModel(pydantic.BaseModel):
    model_config = ConfigDict(
        str_min_length=1,
        str_strip_whitespace=True,
        json_encoders={
            datetime: encode_datetime,
            ObjectId: encode_object_id,
        },
    )


class Auditable(BaseModel):
    created_at: datetime | None = Field(None, title="Data de criação")
    updated_at: datetime | None = Field(None, title="Data de alteração")


class BaseId(BaseModel):
    id: str | None = Field(None, example="630e3bbc950b052e8724491a")
