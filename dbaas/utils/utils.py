from datetime import datetime, timezone

from bson import ObjectId


def utcnow():
    return datetime.now(timezone.utc)


def encode_object_id(recordid: ObjectId):
    return str(recordid)


def encode_datetime(dt: datetime):
    return dt.replace(tzinfo=timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
