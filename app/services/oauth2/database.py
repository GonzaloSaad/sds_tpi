from pymongo import MongoClient
from pymongo.collection import Collection

from .schemas import OAuth2Token

MONGODB_HOST = "localhost"
MONGODB_PORT = 27017


def _get_collection_client() -> Collection:
    client = MongoClient(MONGODB_HOST, MONGODB_PORT)
    sds_db = client.sds
    return sds_db.oauth2_tokens


def insert(user_id: str, token: OAuth2Token):
    collection = _get_collection_client()
    document = {"user_id": user_id, "token": token.dict()}
    collection.insert_one(document=document)


def get_by_user(user_id: str) -> OAuth2Token:
    collection = _get_collection_client()
    document = collection.find_one(filter={"user_id": user_id})
    return OAuth2Token.parse_obj(document["token"])


def update_by_user_id(user_id: str, token: OAuth2Token):
    collection = _get_collection_client()
    collection.update_one(
        filter={"user_id": user_id},
        update={
            "$set":
                {
                    "token": token.dict(),
                },
        }
    )
