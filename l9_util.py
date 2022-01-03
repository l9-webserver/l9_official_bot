import discord
import main
def getRole(name: str) -> discord.Role:
    return discord.utils.get(main.guild.roles, name)
def getRoleId(role: discord.Role) -> int:
    return role.id