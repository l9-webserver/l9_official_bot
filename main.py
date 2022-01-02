import datetime
import json
import random
import re
import threading
import urllib

import discord
import requests
from discord.ext import commands
from discord.message import Message


def checkUploads():
    threading.Timer(15.0, checkUploads).start()


    channel = "https://www.youtube.com/user/PewDiePie"

    html = requests.get(channel + "/videos").text
    info = re.search('(?<={"label":").*?(?="})', html).group()
    date = re.search('\d+ \w+ ago.*seconds ', info).group()
    print(info)
    print(date)

checkUploads()
client = discord.Client()

prefix = '.'
webserver = "https://l9-webserver.github.io/"
config_json = "config_commands.json"

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix=prefix, intents=intents)


def load_json_dict_local(file: str) -> dict:
    return json.loads("".join(open(file, "r").readlines()))

#
#config_commands = load_json_dict_local(config_json)


#command_actions = load_json_dict_local("cmd_actions.json")
#
kanal = 927244830654992495


def getFirstCharOfMessage(message: Message) -> str:
    return str(message.content[0])


def checkMsgAsCmd(message: Message, comp: str) -> bool:
    return message.content.startswith(comp)


@client.event
async def on_ready():
    print("digo se")

pravila_id = 839185411393847299


@client.event
async def on_member_join(member):
    print("join")
    mcount = len([m for m in member.guild.members if not m.bot])
    embedVar = discord.Embed(title=f"Dobrodošao *{member.name}* u L9 Discord server! Pročitaj pravila u *#{client.get_channel(927255993094656102)}* prije nego što nastaviš.",
                             description=f"Član broj {mcount}", color=random.randint(0, 0xffffff))
    await client.get_channel(kanal).send(embed=embedVar)
    # await client.get_channel(kanal).send(f"Dobrodošao <@{member.id}> u L9 Discord server! Pročitaj pravila u <#{pravila_id}> prije nego što nastaviš.\nmember broj 69")


@client.event
async def on_member_remove(member):
    print("leave")
    embedVar = discord.Embed(
        title=f"Zbogom *{member.name}*!", color=random.randint(0, 0xffffff))
    await client.get_channel(kanal).send(embed=embedVar)
# @client.event
# async def on_message(message):
#     if (getFirstCharOfMessage(message) == prefix):
#         for key_subset in config_commands.keys():
#             # print(config_commands[key_subset])
#             for key_command in config_commands[key_subset]:
#                 command = f"{prefix}{key_subset} {key_command}"
#                 command_as_action = f"{key_subset} {key_command}"
#                 if checkMsgAsCmd(message, command):
#                     func = command_actions[command_as_action]
#                     func_obj = globals()[func]
#                     await func_obj(message)

client.run('OTI3MTI4ODMyMTQ4OTA1OTg0.YdFuAg.oNnKaN75SjN8zud9NxP6QITUI4U')
