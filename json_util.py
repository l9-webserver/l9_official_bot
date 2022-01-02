import json


def getDict(json_file: str) -> dict:
    return json.loads("".join(open(json_file, "r").readlines()))


def get(json_file: str, key: str) -> str:
    return getDict(json_file)[key]
