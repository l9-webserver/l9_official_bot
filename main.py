import threading
import json
import random
from urllib.request import urlopen

import discord
from discord import user
from discord.ext import commands
from discord.message import Message
import json_util
from keep_alive import keep_alive

client = discord.Client()

prefix = '.'

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix=prefix, intents=intents)

messages = dict()


def printit():
  threading.Timer(10.0, printit).start()
  global messages
  print(messages)
  messages = dict()


printit()


def getFirstCharOfMessage(message: Message) -> str:
    return str(message.content[0])


def checkMsgAsCmd(message: Message, comp: str) -> bool:
    return message.content.startswith(comp)


@client.event
async def on_ready():
    print("digo se")


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


@client.event
async def on_message(message: Message):
    mval = "message_values.json"
    for key in json_util.getDict(mval).keys():
        user_name = message.author.display_name
        if user_name not in messages.keys():
            messages[user_name]=0
        if key in message.content:
            messages[user_name]+=int(json_util.get(mval, key))*message.content.count(key)
        else:
            messages[user_name]+=1
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
keep_alive()
client.run('OTI3MTI4ODMyMTQ4OTA1OTg0.YdFuAg.oNnKaN75SjN8zud9NxP6QITUI4U')
