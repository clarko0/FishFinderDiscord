import time
import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
import json
from random import randint
from datetime import date, datetime
import os
import asyncio

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix=commands.when_mentioned_or("."), intents=intents)


DB = "/src/ffsrc/db.json"
MEMBERS = "/src/members.json"


def getDataFromDB():
    with open(DB, "r") as readDB:
        zones = json.load(readDB)
    return zones


def sortTier(num):
    if num == 5:
        new = 0
    elif num == 4:
        new = 1
    elif num == 3:
        new = 2
    elif num == 2:
        new = 3
    elif num == 1:
        new = 4
    else:
        new = 5
    return new


def nameSort(num):
    if num == 0:
        name = "Special"
    else:
        name = str(num)
    return name


@client.event
async def on_ready():
    print(f"Loggined in as {client.user}")


def createEmbed(number):
    embed = discord.Embed(
        title=f"Tier {nameSort(number)} - Top 15 results                               ‎",
        color=discord.Color.random(),
    )

    zoneData = ""
    playerData = ""
    feesData = ""

    for i in range(1, 15):
        zoneData = (
            zoneData
            + f'[{getDataFromDB()[sortTier(int(number))][i-1]["zone"]}](https://game.worldofdefish.com/zone/{getDataFromDB()[sortTier(int(number))][i-1]["zone"]}/fishing)\n'
        )

        playerData = (
            playerData + f'{getDataFromDB()[sortTier(int(number))][i-1]["players"]}\n'
        )

        feesData = (
            feesData
            + f'{getDataFromDB()[sortTier(int(number))][i-1]["fee"]}% / {round(getDataFromDB()[sortTier(int(number))][i-1]["wod"], 1)}\n'
        )

    embed.set_thumbnail(url="https://i.ibb.co/s13xKJ5/Fishfinderlogo.png")

    embed.add_field(
        name="Zone",
        value=zoneData,
        inline=True,
    )
    embed.add_field(
        name="Players",
        value=playerData,
        inline=True,
    )
    embed.add_field(
        name="Fees / $WOD per hour",
        value=feesData,
        inline=True,
    )

    return embed


def CreateBasicEmbed(number):
    embed = discord.Embed(
        title=f"Tier {nameSort(number)} - Free Search                              ‎",
        color=discord.Color.random(),
    )
    zoneData = ""
    playerData = ""
    feesData = ""
    zoneData = (
        zoneData
        + f'[{getDataFromDB()[sortTier(int(number))][0]["zone"]}](https://game.worldofdefish.com/zone/{getDataFromDB()[sortTier(int(number))][0]["zone"]}/fishing)\n'
    )

    playerData = (
        playerData + f'{getDataFromDB()[sortTier(int(number))][0]["players"]}\n'
    )

    feesData = (
        feesData
        + f'{getDataFromDB()[sortTier(int(number))][0]["fee"]}% / {round(getDataFromDB()[sortTier(int(number))][0]["wod"], 1)}\n'
    )

    embed.add_field(
        name="Zone",
        value=zoneData,
        inline=True,
    )
    embed.add_field(
        name="Players",
        value=playerData,
        inline=True,
    )
    embed.add_field(
        name="Fees / $WOD per hour",
        value=feesData,
        inline=True,
    )

    embed.add_field(
        name=f"Fish Finder found {randint(2,5)} more zones with 0 players!",
        value="Purchase the full access to Fish Finder **for only $3** to view them and have no search cooldown. Message <@344400439728668672> to order.",
        inline=False,
    )

    return embed


def sortEmoji(string):
    if string.emoji.name == "🟥":
        k = 0
    elif string.emoji.name == "🟨":
        k = 1
    elif string.emoji.name == "🟪":
        k = 2
    elif string.emoji.name == "🟦":
        k = 3
    elif string.emoji.name == "⬜":
        k = 4
    elif string.emoji.name == "⬛":
        k = 5
    else:
        print("ERROR")
    return k


@client.command()
async def setup(ctx):
    open("channel.json", "w").close()
    origin = await ctx.send("**CHOOSE YOUR TIER**")
    with open("channel.json", "a") as writeJson:
        writeJson.write(
            "{\n"
            + '"messageID" : '
            + str(origin.id)
            + ",\n"
            + '"channelID" : '
            + str(origin.channel.id)
            + "\n}"
        )
    emojis = ["🟥", "🟨", "🟪", "🟦", "⬜", "⬛"]
    emojis.reverse()
    for emoji in emojis:
        await origin.add_reaction(emoji)
        time.sleep(0.1)


def CreateSearchEmbed(number):
    embed = discord.Embed(
        color=discord.Color.random(),
    )
    embed.add_field(
        name=f"Search started: results will be sent in {number} seconds.                              ‎",
        inline=False,
        value="Purchase full access to Fish Finder **for only $3** to skip cooldown.",
    )

    return embed


@client.command()
async def addmembership(ctx, arg1, arg2, arg3):
    author = ctx.message.author
    if author.id == 344400439728668672:
        with open("members.json", "r") as f:
            data = json.load(f)
        id = arg1
        members = []
        length = arg2
        type = arg3
        date = datetime.today()
        date = str(date)
        try:
            obj = {
                "id": id,
                "length": f"{length}",
                "type": type,
                "date": date,
            }
        except:
            await ctx.send("Error.")
        members.append(obj)
        for item in data["members"]:
            members.append(item)
        with open("members.json", "r") as f:
            data = json.load(f)
            data["members"] = members
        with open("members.json", "w") as f:
            json.dump(data, f, indent=1)
        await ctx.send(f"Added <@{id}> to database: for {length} month")
    else:
        await ctx.send("Error, you need to be an admin to use this role")


LOGS = 1012378872995655760

EVERYOTHER = True


@client.event
async def on_raw_reaction_add(payload):
    with open(MEMBERS, "r") as f:
        data2 = json.load(f)
    with open("channel.json", "r") as readJson:
        data = json.load(readJson)
    CHANNEL = data["channelID"]
    members = []
    MSG_ID = data["messageID"]
    for item in data2["members"]:
        members.append(int(item["id"]))
    member = await client.fetch_user(payload.member.id)
    channel = await client.fetch_channel(CHANNEL)
    message = await channel.fetch_message(MSG_ID)
    if payload.channel_id == CHANNEL:
        if payload.message_id == MSG_ID:
            if payload.member.bot != True:
                if member.id in members:
                    try:
                        await message.remove_reaction(
                            member=member, emoji=payload.emoji.name
                        )
                        if member.dm_channel is None:
                            await member.create_dm()
                        await member.dm_channel.send(
                            embed=createEmbed(sortEmoji(payload))
                        )
                        log_channel = await client.fetch_channel(LOGS)
                        await log_channel.send(
                            f"**<@{payload.member.id}> just searched Tier {nameSort(sortEmoji(payload))}**",
                        )

                    except:
                        pass
                else:
                    try:
                        num = randint(40, 61)
                        await message.remove_reaction(
                            member=member, emoji=payload.emoji.name
                        )
                        if member.dm_channel is None:
                            await member.create_dm()
                        await member.dm_channel.send(embed=CreateSearchEmbed(num))
                        await asyncio.sleep(num)
                        await member.dm_channel.send(
                            embed=CreateBasicEmbed(sortEmoji(payload))
                        )
                        log_channel = await client.fetch_channel(LOGS)
                        await log_channel.send(
                            f"**<@{payload.member.id}> just searched Tier {nameSort(sortEmoji(payload))}**"
                        )
                    except:
                        pass


if __name__ == "__main__":
    client.run(
        os.getenv("BOT_TOKEN")
    )
