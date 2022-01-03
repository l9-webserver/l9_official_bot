import pymongo, json

from pymongo import collection


class webserver:
    client = pymongo.MongoClient(
        "mongodb+srv://l9-bot:l9-official_3122@cluster0.d2lnd.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client["discord"]
    collection_db = db["l9-bot-data"]

    def postJson(json_str: str, id: int):
        dict_=json.loads(json_str)
        dict_["_id"]=id
        webserver.collection_db.insert_one(dict_)

    def post(data: dict, id: int):
        data_=data
        data_["_id"]=id
        webserver.collection_db.insert_one(data_)

    def update(name: str, key: str, value):
        webserver.collection_db.update_one({"name": name}, {"$set": {key: value}})
    def get(name: str) -> dict:
        ret: dict=webserver.collection_db.find_one({"name": name})
        return ret
