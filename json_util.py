import json


def readls(json_file: str) -> str:
    return "".join(open(json_file, "r").readlines())


def getDict(json_file: str) -> dict:
    return json.loads(readls(json_file))


def get(json_file: str, key: str) -> str:
    return getDict(json_file)[key]
