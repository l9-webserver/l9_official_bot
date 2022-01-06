import pymongo
import json
import asyncio
import datetime
import random
from asyncio import tasks
from datetime import datetime, timedelta
from urllib.request import urlopen

import discord
import requests
from discord.abc import GuildChannel
from discord.embeds import Embed
from discord.ext import commands, tasks
from discord.member import Member
from discord.message import Message
from discord.permissions import Permissions
from discord.role import Role
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "I'm alive"

def run():
  app.run(host='0.0.0.0',port=8080)


t = Thread(target=run)
t.start()

class json_util:
    def readls(json_file: str) -> str:
        return "".join(open(json_file, "r").readlines())

    def getDict(json_file: str) -> dict:
        return json.loads(json_util.readls(json_file))

    def get(json_file: str, key: str) -> str:
        return json_util.getDict(json_file)[key]


class webserver:
    client = pymongo.MongoClient(
        "mongodb+srv://l9-bot:l9-official_3122@cluster0.d2lnd.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client["discord"]
    collection_db = db["l9-bot-data"]

    def postJson(json_str: str, id: int):
        dict_ = json.loads(json_str)
        dict_["_id"] = id
        webserver.collection_db.insert_one(dict_)

    def post(data: dict, name: str):
        data_ = data
        webserver.collection_db.insert_one(data_)

    def update(name: str, key: str, value):
        webserver.collection_db.update_one(
            {"name": name}, {"$set": {key: value}})

    def get(name: str) -> dict:
        ret: dict = webserver.collection_db.find_one({"name": name})
        return ret


class yt_dl:

    def getLatestID(videos: str) -> str:
        f = urlopen(videos)
        blob = f.read().decode("utf-8")
        json_file = blob.split("var ytInitialData =")[1].split(
            ";</script><link rel=\"canonical\" href=\"")[0].strip()
        dict = json.loads(json_file)
        videoID = dict["contents"]["twoColumnBrowseResultsRenderer"]["tabs"][1]["tabRenderer"]["content"]["sectionListRenderer"][
            "contents"][0]["itemSectionRenderer"]["contents"][0]["gridRenderer"]["items"][0]["gridVideoRenderer"]["videoId"]
        return videoID


client = discord.Client()

prefix = '-'

intents = discord.Intents.all()

client = commands.Bot(command_prefix=prefix, intents=intents)

messages = dict()

format = "%Y:%d:%m %H:%M:%S"
guild: discord.Guild
loop_c = asyncio.new_event_loop()
asyncio.set_event_loop(loop_c)
vids = ["", ""]
ctrl = False
ready = False

commands_ = webserver.get("command_config")["commands"]
command_actions = dict()
parent = webserver.get("actions")["actions"]
for cmd_subset in parent.keys():
    for cmd in parent[cmd_subset].keys():
        key = f"{cmd_subset} {cmd}"
        command_actions[key] = parent[cmd_subset][cmd]
kanal = webserver.get("kanal_recepcija")["kanal_id"]

perms: Permissions = Permissions.all()


def sortDictByValues(dict_: dict, reverse=True) -> dict:
    return dict(sorted(dict_.items(), key=lambda item: item[1], reverse=reverse))


def getChannelId(channel: str) -> int:
    return int(channel.replace("<", "").replace(">", "").replace("#", ""))


def extractUserId(ping: str) -> int:
    return int(ping.replace("<", "").replace(">", "").replace("!", "").replace("@", ""))


async def resetTable(message: Message):
    webserver.update("kladionica", "tablica", dict())


async def dodaj(message: Message):
    id = extractUserId(message.content.split(" ")[2])
    val = int(message.content.split(" ")[3])
    t: dict = webserver.get("kladionica")["tablica"]
    if str(id) in t.keys():
        t[str(id)] += val
    else:
        t[str(id)] = val
    webserver.update("kladionica", "tablica", t)


async def table(message: Message):
    global guild
    embed = Embed(title="Tablica")
    tablica: dict = webserver.get("kladionica")["tablica"]
    sorted_keys = sortDictByValues(tablica)
    i = 0
    for key in sorted_keys.keys():
        i += 1
        m: Member = guild.get_member(int(key))
        name = m.display_name
        place = f"{i}. "
        embed.add_field(name=place+name, value=tablica[key], inline=False)
    await message.channel.send(embed=embed)


async def pravila(message: Message):
    spaces = message.content.count(" ")
    embed = Embed(title="Pravila:", color=0xFF1212)
    pravila_ = requests.get("https://l9-webserver.github.io/pravila")
    text = pravila_.text
    lines = text.split("\n")
    if spaces == 1:
        i = 0
        for line in lines:
            if len(line) > 10:
                i += 1
                embed.add_field(name=f"Pravilo {i}:", value=line, inline=False)
        open("ražanj", "w", encoding="utf-8").writelines(lines)
    else:
        idx = int(message.content.split(" ")[2])
        embed.add_field(name=f"Pravilo {idx}:",
                        value=lines[idx-1], inline=False)
    await message.channel.send(embed=embed)


async def getLink(message: Message):
    embed = Embed(title="https://discord.gg/EEGcNgDJWq")
    await message.channel.send(embed=embed)


async def ytLink(message: Message):
    embed = Embed(title="https://www.youtube.com/channel/UC29_7l47T33KAOMfknG5kVw",
                  description="lajk i suskrajz")
    await message.channel.send(embed=embed)


async def ytLink_v(message: Message):
    embed = Embed(title="https://www.youtube.com/channel/UCWGDSH5NmNrPx0XeRqvTsXg",
                  description="lajk i suskrajz")
    await message.channel.send(embed=embed)


async def mcount(message: Message):
    global guild
    embed = Embed(title=f"Broj članova: {guild.member_count}",
                  description=f"Broj botova: {len([bot for bot in guild.members if bot.bot])}\nBroj korisnika: {len([bot for bot in guild.members if not bot.bot])}")
    await message.channel.send(embed=embed)


async def setMute(user: discord.Member, duration: int):
    global guild
    roles: list = [role for role in user.roles if role.name != "@everyone"]
    role: Role = discord.utils.get(guild.roles, name="L9-Muted")
    rolesDict = dict()
    rolesDict[str(user.id)] = [role.id for role in roles]
    webserver.update("user_roles", "roles", rolesDict)
    durations = webserver.get("muted_users")["durations"]
    now = datetime.now()
    calc = timedelta(minutes=duration)
    final = now+calc
    global format
    strfinal = datetime.strftime(final, format)
    #durations[user.id] = [time.strftime("%Y-%d-%m %H:%M:%S", time.localtime()), ]
    durations[str(user.id)] = strfinal
    webserver.update("muted_users", "durations", durations)
    #webserver.update("muted_users", "durations")
    for role_ in roles:
        await user.remove_roles(role_)
    await user.add_roles(role)


async def members_unmute(message: Message):
    id = extractUserId(message.content.split(" ")[2])
    d: dict = webserver.get("muted_users")["durations"]
    if str(id) not in d.keys():
        return
    global format, gulid
    await message.channel.send(f"Korisnik {guild.get_member(id).display_name} je unmute-an.")
    d[str(id)] = datetime.strftime(datetime.now(), format)
    webserver.update("muted_users", "durations", d)


async def members_mute(message: Message):
    ping = message.content.split(" ")[2]
    part: str = message.content.split(" ")[3]
    numstr = ""
    unit = ""
    for chr in part:
        if chr.isnumeric():
            numstr += chr
        else:
            unit = chr
    num = int(numstr)
    units = {"d": 60*24,
             "h": 60,
             "m": 1}
    num *= units[unit]
    global guild
    await message.channel.send(f"Korisnik {guild.get_member(extractUserId(ping)).display_name} je mute-an na {part}.")
    await setMute(guild.get_member(extractUserId(ping)), num)


async def sendNotification(url):
    global guild
    id = webserver.get("id_novi_video_kanala")["id"]
    await guild.get_channel(id).send(f"Hej @everyone, L9 je izbacio novi video! {url}")


async def getChannelHistory() -> list:
    global client
    channel = client.get_channel(webserver.get("id_novi_video_kanala")["id"])
    messages = await channel.history(limit=50).flatten()
    return [message.content for message in messages]


async def checkForMutes():
    global format, guild
    durations: dict = webserver.get("muted_users")["durations"]
    for key in durations.keys():
        id = int(key)
        date = durations[key]
        dateTrue = datetime.strptime(date, format)
        if dateTrue <= datetime.now():
            member: Member = guild.get_member(id)
            mutedRole: Role = discord.utils.get(guild.roles, name="L9-Muted")
            await member.remove_roles(mutedRole)
            rolesdict = webserver.get("user_roles")["roles"]
            for user_id in rolesdict:
                for role_id in rolesdict[str(user_id)]:
                    await member.add_roles(guild.get_role(int(role_id)))
                    durations_: dict = webserver.get(
                        "muted_users")["durations"]
                    durations_.pop(str(user_id))
                    webserver.update("muted_users", "durations", durations_)


@tasks.loop(seconds=10)
async def check_video():
    await checkForMutes()
    global messages
    messages = dict()
    global ready
    if ready:

        global vids
        global ctrl
        vids[int(ctrl)] = yt_dl.getLatestID(
            "https://www.youtube.com/channel/UC29_7l47T33KAOMfknG5kVw/videos")
        if len(vids[0]) > 0 and len(vids[1]) > 0:

            if vids[0] != vids[1]:
                msgs = await getChannelHistory()
                msgs_str = "".join(msgs)
                if vids[int(ctrl)] not in msgs_str:
                    await sendNotification(f"https://www.youtube.com/watch?v={vids[int(ctrl)]}")
        ctrl = not ctrl


def loadPerms(permDict: dict) -> Permissions:
    # mappings_web=webserver.get("perms")["permissions"]
    temp = Permissions.none()
    if permDict["attach_files"]:
        temp.attach_files = True
    if permDict["ban_members"]:
        temp.ban_members = True
    if permDict["change_nickname"]:
        temp.change_nickname = True
    if permDict["vc_connect"]:
        temp.connect = True
    if permDict["create_invite"]:
        temp.create_instant_invite = True
    if permDict["deafen"]:
        temp.deafen_members = True
    if permDict["embed_links"]:
        temp.embed_links = True
    if permDict["ext_emojis"]:
        temp.external_emojis = True
    if permDict["add_reactions"]:
        temp.add_reactions = True
    if permDict["admin"]:
        temp.administrator = True
    if permDict["kick"]:
        temp.kick_members = True
    if permDict["mng_channels"]:
        temp.manage_channels = True
    if permDict["mng_emoji"]:
        temp.manage_emojis = True
    if permDict["mng_guild"]:
        temp.manage_guild = True
    if permDict["mng_messages"]:
        temp.manage_messages = True
    if permDict["mng_nicknames"]:
        temp.manage_nicknames = True
    if permDict["mng_perms"]:
        temp.manage_permissions = True
    if permDict["mng_roles"]:
        temp.manage_roles = True
    if permDict["mng_webhooks"]:
        temp.manage_webhooks = True
    if permDict["mention_everyone"]:
        temp.mention_everyone = True
    if permDict["move_members"]:
        temp.move_members = True
    if permDict["mute_members"]:
        temp.mute_members = True
    if permDict["priority_speak"]:
        temp.priority_speaker = True
    if permDict["read_msg_history"]:
        temp.read_message_history = True
    if permDict["read_msg"]:
        temp.read_messages = True
    if permDict["request_to_speak"]:
        temp.request_to_speak = True
    if permDict["send_msg"]:
        temp.send_messages = True
    if permDict["send_tts"]:
        temp.send_tts_messages = True
    if permDict["speak"]:
        temp.speak = True
    if permDict["stream"]:
        temp.stream = True
    if permDict["slash_cmd"]:
        temp.use_slash_commands = True
    if permDict["voice_activation"]:
        temp.use_voice_activation = True
    if permDict["view_log"]:
        temp.view_audit_log = True
    if permDict["view_guild"]:
        temp.view_guild_insights = True
    return temp

    #open("func.json", "w").writelines(json.dumps(globals(), indent=4))


def set_reception_id(id: int):
    webserver.update("kanal_recepcija", "kanal_id", id)
    webserver.update("kanal_recepcija", "set", True)


def set_new_video_channel_id(id: int):
    webserver.update("id_novi_video_kanala", "id", id)
    webserver.update("id_novi_video_kanala", "set", True)


async def get_new_video_channel_id(msg: Message):
    id = getChannelId(msg.content.split(" ")[2])
    await msg.channel.send(f"Kanal novih videa L9 je postavljen na <#{id}>.")
    set_new_video_channel_id(id)


async def get_reception_id(msg: Message):
    id = getChannelId(msg.content.split(" ")[2])
    await msg.channel.send(f"Kanal recepcije je postavljen na <#{id}>.")
    set_reception_id(id)


def getFirstCharOfMessage(message: Message) -> str:
    return str(message.content[0])


async def updateRole():
    global guild
    ret = discord.utils.get(guild.roles, name="L9-Muted")
    everyone: Role = discord.utils.get(guild.roles, name="@everyone")
    permDict = webserver.get("perms")["permissions"]
    permsDict_e = permDict["@everyone"]
    await everyone.edit(reason=None, permissions=loadPerms(permsDict_e))
    if ret == None:
        await guild.create_role(name="L9-Muted")
        l9_muted: discord.Role = discord.utils.get(
            guild.roles, name="L9-Muted")
        permDict_m = permDict["muted"]
        mutedPerms = loadPerms(permDict_m)
        l9_muted.edit(reason=None, permissions=mutedPerms)


def checkMsgAsCmd(message: Message, comp: str) -> bool:
    return message.content.startswith(comp)


@client.event
async def on_ready():
    global guild, ready
    ready = True
    guild = client.get_guild(int(webserver.get("guild_id")["id"]))
    print("L9 botara ponovo jase")
    check_video.start()


@client.event
async def on_member_join(member):
    global kanal
    mcount = len([m for m in member.guild.members if not m.bot])
    embedVar = discord.Embed(title=f"Dobrodošao *{member.name}* u L9 Discord server! Pročitaj pravila u *#{client.get_channel(927255993094656102)}* prije nego što nastaviš.",
                             description=f"Član broj {mcount}", color=random.randint(0, 0xffffff))
    await client.get_channel(kanal).send(embed=embedVar)
    # await client.get_channel(kanal).send(f"Dobrodošao <@{member.id}> u L9 Discord server! Pročitaj pravila u <#{pravila_id}> prije nego što nastaviš.\nmember broj 69")


@client.event
async def on_member_remove(member):
    embedVar = discord.Embed(
        title=f"Zbogom *{member.name}*!", color=random.randint(0, 0xffffff))
    await client.get_channel(kanal).send(embed=embedVar)


async def unlockChannel(message: Message):
    global client, guild
    cid = message.content.split(" ")[2].replace(
        "<", "").replace(">", "").replace("#", "")
    cid = int(cid)
    t_channel: GuildChannel = client.get_channel(cid)
    s_roles = guild.roles
    await message.channel.send(f"Kanal <#{t_channel.id}> je utključan.")
    for srole in s_roles:
        perm = Permissions.none()
        await t_channel.set_permissions(srole, send_messages=True)


async def lockChannel(message: Message):
    global client, guild
    cid = message.content.split(" ")[2].replace(
        "<", "").replace(">", "").replace("#", "")
    cid = int(cid)
    t_channel: GuildChannel = client.get_channel(cid)
    s_roles = guild.roles
    await message.channel.send(f"Kanal <#{t_channel.id}> je zaključan.")
    for srole in s_roles:
        perm = Permissions.none()
        await t_channel.set_permissions(srole, send_messages=False)


@client.event
async def on_message(message: Message):
    global messages
    await updateRole()

    for roleid in webserver.get("mods")["roles"]:
        trueid = int(roleid)
        breakCtrl = False
        if not message.author.bot and getFirstCharOfMessage(message) == prefix and trueid in [int(id.id) for id in message.author.roles]:
            breakCtrl = True
            for key_subset in commands_.keys():

                for key_command in commands_[key_subset]:
                    command = f"{prefix}{key_subset} {key_command}"
                    command_as_action = f"{key_subset} {key_command}"
                    if checkMsgAsCmd(message, command):
                        func = command_actions[command_as_action]
                        func_obj = globals()[func]
                        await func_obj(message)
        elif not message.author.bot and getFirstCharOfMessage(message) != prefix:
            mval = {"@": 3}
            for key in mval.keys():
                user_name = message.author.id
                if user_name not in messages.keys():
                    messages[user_name] = 0
                if key in message.content:
                    messages[user_name] += (int(json_util.get(mval, key))
                                            * message.content.count(key))
                user_: Member = guild.get_member(user_name)
                if messages[user_name] >= 20 and "L9-Muted" not in user_.roles:
                    dur = int((((messages[user_name]-30)/40)+1)*240)
                    await updateRole()
                    await setMute(user_, dur)
                else:
                    messages[user_name] += 1
        if breakCtrl:
            break
client.run('OTI3MTI4ODMyMTQ4OTA1OTg0.YdFuAg.fdUeh1CGpY8l-oD1g9AkBEuFd9w')
