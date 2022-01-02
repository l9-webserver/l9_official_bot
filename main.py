import discord
from discord.message import Message
import json
import requests
import urllib
client = discord.Client()

prefix = '.'
webserver = "https://l9-webserver.github.io/"
config_json = "config_commands.json"


def load_json_dict_local(file: str) -> dict:
    return json.loads("".join(open(file, "r").readlines()))


config_commands = load_json_dict_local(config_json)

command_actions = load_json_dict_local("cmd_actions.json")


def getFirstCharOfMessage(message: Message) -> str:
    return str(message.content[0])


def checkMsgAsCmd(message: Message, comp: str) -> bool:
    return message.content.startswith(comp)


def POST(url: str, data_str: str):
    data = {"data": data_str}
    requests.post(url, data)


def GET_JSON(web: str) -> dict:
    with urllib.request.urlopen(f"{webserver}{web}") as url:
        data = json.loads(url.read().decode())
        return data


async def CMD_getChannelId(message: Message):
    id = int(message.content.split(" ")[2])
    id_cfg={
        "id": id
    }

    ret=POST(webserver+"notification.json", json.dumps(id_cfg))
    await message.channel.send(json.dumps(id_cfg, indent=4))
@client.event
async def on_ready():
    print("digo se")


# @client.event
# async def on_member_join(member):


@client.event
async def on_message(message):
    if (getFirstCharOfMessage(message) == prefix):
        for key_subset in config_commands.keys():
            # print(config_commands[key_subset])
            for key_command in config_commands[key_subset]:
                command = f"{prefix}{key_subset} {key_command}"
                command_as_action = f"{key_subset} {key_command}"
                if checkMsgAsCmd(message, command):
                    func = command_actions[command_as_action]
                    func_obj = globals()[func]
                    await func_obj(message)
client.run('OTI3MTI4ODMyMTQ4OTA1OTg0.YdFuAg.570w8q0biNBgWcHzYfWfy5xR4N0')
