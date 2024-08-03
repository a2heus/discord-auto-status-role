import discord
from discord.ext import commands, tasks

TOKEN = 'YOUR TOKEN'

GUILD_ID = 123456789
ROLE_ID = 123456789
LINK = ".gg/1234567890"

intents = discord.Intents.default()
intents.members = True  
intents.presences = True 

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Connected as {bot.user}')
    guild = bot.get_guild(GUILD_ID)
    if guild is not None:
        status_checker.start(guild)  
    else:
        print("The bot is not on the server.")

@tasks.loop(seconds=1)  
async def status_checker(guild):
    role = guild.get_role(ROLE_ID)
    if role is None:
        print("This role does not exist.")
        return

    for member in guild.members:
        await check_member_status(member, role)

async def check_member_status(member, role):
    has_link = False
    if member.activity and member.activity.type == discord.ActivityType.custom:
        if member.activity.state and LINK in member.activity.state:
            has_link = True

    if has_link:
        if role not in member.roles:
            try:
                await member.add_roles(role)
                print(f"Added role to {member.name}")
            except Exception as e:
                print(f"Error while adding the role to {member.name}: {e}")
    else:
        if role in member.roles:
            try:
                await member.remove_roles(role)
                print(f"Role removed {member.name}")
            except Exception as e:
                print(f"Error while removing the rome of {member.name}: {e}")

@bot.event
async def on_member_update(before, after):
    guild = after.guild
    role = guild.get_role(ROLE_ID)
    if role is None:
        print("This role does not exist.")
        return

    await check_member_status(after, role)

bot.run(TOKEN)
