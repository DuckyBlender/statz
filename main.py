import discord
from discord.ext import commands, tasks
import json, time, asyncio
from datetime import datetime

description = "A simple statistics bot made by DuckyBlender#0001"

token = open('token.txt', 'r').read()

intents = discord.Intents().all()

bot = commands.Bot(command_prefix=commands.when_mentioned_or('.'), description=description, intents=intents)

uzytkownicy_id = 986637437788909668
online_id = 987293504298450984
maxonline_id = 986637678940389396
najnowszyczlonek_id = 1002606503909412995
ilewgulagu_id = 986638188216987670
lastupdated_id = 987760403884953620

gulagroleid = 933662960977580032


# === ON START ===
@bot.event
async def on_ready():
        print("\n".join([
            f"",
            f"Logged in as: {bot.user.name} - {bot.user.id}",
            f"Version: {discord.__version__}"
        ]))
        formatted_guilds = [
            f"Name: {g.name} - ID: {g.id} - Members: {g.member_count}"
            for g in bot.guilds
        ]
        guild_string = "\n".join(formatted_guilds)
        print("\n".join([
            f"-> Active on {len(bot.guilds)} guilds",
            f"-> {len(set(bot.get_all_members()))} unique members ({sum(g.member_count for g in bot.guilds)} total)",
            f"\n"
            f"=== LIST OF GUILDS ===",
            f"{guild_string}\n"
            f"======================"
            f"\n"
        ]))
        update_stats.start()

# == UPDATE STATS ===
@tasks.loop(minutes=10)
async def update_stats():
    print("Updating stats...")
    await bot.wait_until_ready()

    # Write stats to json file
    with open('stats.json', 'r') as f:
        stats = json.load(f)

    stats['members'] = len(set(bot.get_all_members()))

    # Get online members excluding bots
    onlineCount = 0
    for member in bot.get_all_members():
        if not member.bot and member.status != discord.Status.offline:
            onlineCount += 1
    print(f"Online: {onlineCount}")
    stats['online'] = onlineCount
    
    onlineCount = 0
    for x in bot.get_all_members():
        if x.status != discord.Status.offline:
            onlineCount += 1
    
    # Remove bots from online count
    onlineCount = onlineCount

    if stats['online'] > stats['maxonline']:
        stats['maxonline'] = stats['online']

    gulagrole = discord.utils.get(bot.guilds[0].roles, id=gulagroleid)
    stats['gulagcount'] = len(gulagrole.members)
    
    with open('stats.json', 'w') as f:
        json.dump(stats, f, indent=4)

    uzytkownicy = bot.get_channel(uzytkownicy_id)
    online = bot.get_channel(online_id)
    maxonline = bot.get_channel(maxonline_id)
    najnowszyczlonek = bot.get_channel(najnowszyczlonek_id)
    ilewgulagu = bot.get_channel(ilewgulagu_id)
    lastupdated = bot.get_channel(lastupdated_id)

    # Send stats to name channel
    await uzytkownicy.edit(name=f"👥・Użytkownicy: {stats['members']}")
    await online.edit(name=f"👀・Online: {stats['online']}")
    await maxonline.edit(name=f"🔥・Max Online: {stats['maxonline']}")
    await ilewgulagu.edit(name=f"💀・Gulag: {stats['gulagcount']}")
    await najnowszyczlonek.edit(name=f"👋・{stats['najnowszy']}")
    await lastupdated.edit(name=f"🔁・{datetime.now().strftime('%H:%M:%S')}")

    

    activity = discord.Activity(name=f"over {len(bot.guilds)} guilds and {len(bot.users)} users!", type=discord.ActivityType.watching)
    await bot.change_presence(activity=activity)

    print(f"Stats updated! [{datetime.now().strftime('%H:%M:%S')}]")

    # Kill the bot (for crontab)
#    await bot.logout()

# === EVENTS ===
@bot.event
async def on_member_join(member):
    with open('stats.json', 'r') as f:
        stats = json.load(f)
    stats['najnowszy'] = member.name

    with open('stats.json', 'w') as f:
        json.dump(stats, f, indent=4)
    

bot.run(token)