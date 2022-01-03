import asyncio
import json
import random
import threading
from asyncio.windows_events import NULL
from urllib.request import urlopen

import discord
from discord import user
from discord import permissions
from discord.ext import commands
from discord.guild import Guild
from discord.message import Message
from discord.permissions import Permissions, permission_alias
from discord.role import Role
import yt_dl
import json_util
from keep_alive import keep_alive
from webserver import webserver

client = discord.Client()

prefix = '.'

intents = discord.Intents.all()

client = commands.Bot(command_prefix=prefix, intents=intents)

messages = dict()

guild: discord.Guild = NULL

# def mute_user(hours: int, ):
#def_mute_duration=int(json_util.get("mute_duration.json", "duration"))
vids=["", ""]
ctrl=False

async def sendNotification():
    global guild
    await guild.get_channel(webserver.get("id_novi_video_kanala")["id"]).send("novi video brateee")
def loop():
    threading.Timer(10.0, loop).start()
    global vids
    global ctrl
    vids[int(ctrl)]=yt_dl.getLatestID("https://www.youtube.com/channel/UC14v0SCbW_c38GjRsF4S1yg/videos")
    print(vids)
    if len(vids[0])>0 and len(vids[1])>0:
        if vids[0] != vids[1]:
            asyncio.run(sendNotification())
    ctrl=not ctrl
loop()
async def setMute(user: discord.Member):
    global guild
    role = discord.utils.get(guild.roles, name="L9-Muted")
    await user.add_roles(role)

perms: Permissions = Permissions.all()


def loadPerms(permDict: dict) -> Permissions:
    # mappings_web=webserver.get("perms")["permissions"]
    mappings = {
        "attach_files": Permissions.attach_files,
        "ban_members": Permissions.ban_members,
        "change_nickname": Permissions.change_nickname,
        "vc_connect": Permissions.connect,
        "create_invite": Permissions.create_instant_invite,
        "deafen": Permissions.deafen_members,
        "embed_links": Permissions.embed_links,
        "ext_emojis": Permissions.external_emojis,
        "add_reactions": Permissions.add_reactions,
        "admin": Permissions.administrator,
        "kick": Permissions.kick_members,
        "mng_channels": Permissions.manage_channels,
        "mng_emoji": Permissions.manage_emojis,
        "mng_guild": Permissions.manage_guild,
        "mng_messages": Permissions.manage_messages,
        "mng_nicknames": Permissions.manage_nicknames,
        "mng_perms": Permissions.manage_permissions,
        "mng_roles": Permissions.manage_roles,
        "mng_webhooks": Permissions.manage_webhooks,
        "mention_everyone": Permissions.mention_everyone,
        "move_members": Permissions.move_members,
        "mute_members": Permissions.mute_members,
        "priority_speak": Permissions.priority_speaker,
        "read_msg_history": Permissions.read_message_history,
        "read_msg": Permissions.read_messages,
        "request_to_speak": Permissions.request_to_speak,
        "send_msg": Permissions.send_messages,
        "send_tts": Permissions.send_tts_messages,
        "speak": Permissions.speak,
        "stream": Permissions.stream,
        "slash_cmd": Permissions.use_slash_commands,
        "voice_activation": Permissions.use_voice_activation,
        "view_log": Permissions.view_audit_log,
        "view_guild": Permissions.view_guild_insights
    }
    lines=[key+"\n" for key in mappings.keys()]
    open("permList.txt", "w").writelines(lines)
    #open("func.json", "w").writelines(json.dumps(globals(), indent=4))


def set_reception_id(id: int):
    webserver.update("kanal_recepcija", "kanal_id", id)
    webserver.update("kanal_recepcija", "set", True)

def set_new_video_channel_id(id: int):
    webserver.update("id_novi_video_kanala", "id", id)
    webserver.update("id_novi_video_kanala", "set", True)
def get_new_video_channel_id(msg: Message):
    id = int(msg.content.split(" ")[2])
    set_new_video_channel_id(id)

def get_reception_id(msg: Message):
    id = int(msg.content.split(" ")[2])
    set_reception_id(id)


def set_member_role_id(id: int):
    webserver.update("id_clan_uloge", "id", id)
    webserver.update("id_clan_uloge", "set", True)


def get_member_role_id(msg: Message):
    id = int(msg.content.split(" ")[2])


def getFirstCharOfMessage(message: Message) -> str:
    return str(message.content[0])


kanal = webserver.get("kanal_recepcija")["kanal_id"]


async def updateRole():
    global guild
    ret = discord.utils.get(guild.roles, name="L9-Muted")
    everyone: Role = discord.utils.get(guild.roles, name="@everyone")
    everyone.permissions.all()
    if ret == None:
        await guild.create_role(name="L9-Muted")
        l9_muted: discord.Role = discord.utils.get(
            guild.roles, name="L9-Muted")
    l9_muted.permissions.none()


def checkMsgAsCmd(message: Message, comp: str) -> bool:
    return message.content.startswith(comp)


commands_ = webserver.get("command_config")["commands"]
command_actions = dict()
parent = webserver.get("actions")["actions"]
for cmd_subset in parent.keys():
    for cmd in parent[cmd_subset].keys():
        key = f"{cmd_subset} {cmd}"
        command_actions[key] = parent[cmd_subset][cmd]


@client.event
async def on_ready():
    print("digo se")
    global guild
    guild = client.get_guild(839185411393847296)


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
        user_name = message.author.id
        if user_name not in messages.keys():
            messages[user_name] = 0
        if key in message.content:
            messages[user_name] += int(json_util.get(mval, key)) * \
                message.content.count(key)
        user_ = guild.get_member(user_name)
        if messages[user_name] >= 50:
            await updateRole()
            await setMute(user_)
        else:
            messages[user_name] += 1
    if (getFirstCharOfMessage(message) == prefix):
        for key_subset in commands_.keys():
            # print(commands_[key_subset])
            for key_command in commands_[key_subset]:
                command = f"{prefix}{key_subset} {key_command}"
                command_as_action = f"{key_subset} {key_command}"
                if checkMsgAsCmd(message, command):
                    func = command_actions[command_as_action]
                    func_obj = globals()[func]
                    func_obj(message)
keep_alive()
client.run('OTI3MTI4ODMyMTQ4OTA1OTg0.YdFuAg.oNnKaN75SjN8zud9NxP6QITUI4U')
