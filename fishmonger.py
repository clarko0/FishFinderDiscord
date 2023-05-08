from ast import arguments
from operator import index
import time
import traceback
import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
import json
from random import randint
from datetime import date, datetime
import asyncio
import requests

client = commands.Bot(command_prefix=commands.when_mentioned_or("."))
MEMBERS = "src/members.json"
CONFIG = "src/fmsrc/config.json"
DATA = "src/fmsrc/data.json"


def GetItems(str):
    obj = {"filters": {"name": str}}
    response = json.loads(
        requests.post(
            "https://api.worldofdefish.com/marketplace/search/items", json=obj
        ).text
    )
    print(response)
    items = []
    for item in response["items"]:
        obj = {
            "name": item["name"],
            "type": item["slot_key"],
            "price": item["order"]["price"] * 1.015,
            "auction": item["order"]["auction"],
            "id": item["id"],
        }
        items.append(obj)
    with open(DATA, "r") as f:
        data = json.load(f)
        data["items"] = items
    with open(DATA, "w") as f:
        json.dump(data, f, indent=1)


def CreateAlertsEmbed(obj):
    embed = discord.Embed(
        title=f"Alerts             ‎",
        color=discord.Color.random(),
    )
    try:
        keywords = "\n".join(obj["keywords"])
        embed.add_field(name=f"Keywords:", value=keywords, inline=False)
    except:
        embed.add_field(name="Keywords:", value="You have no keywords", inline=False)
    return embed


def CreateAddEmbed(str):
    embed = discord.Embed(
        title=f"Added '{str}' to your alerts.", color=discord.Color.random()
    )
    return embed


def CreateRemEmbed(str):
    embed = discord.Embed(
        title=f"Removed '{str}' from your alerts.", color=discord.Color.random()
    )
    return embed


def CreateClearEmbed():
    embed = discord.Embed(title="Cleared your alerts!", color=discord.Color.random())
    return embed


def CreateNoAlertsEmbed():
    embed = discord.Embed(title="You have no alerts set!", color=discord.Color.random())
    return embed


def SearchMain():
    with open(CONFIG, "r") as f:
        data = json.load(f)
    for item in data["configs"]:
        if item["keywords"] != []:
            for i in item["keywords"]:
                print(i)
                GetItems(i)


@client.command()
async def addalert(ctx, *args):
    author = ctx.message.author
    with open(MEMBERS, "r") as f:
        data = json.load(f)
    for item in data["members"]:
        if str(author.id) == item["id"]:
            with open(CONFIG, "r") as f:
                data = json.load(f)
                for item in data["configs"]:
                    if item["id"] == str(author.id):
                        keywords = []
                        arguments = " ".join(args)
                        keywords.append(arguments)
                        for i in item["keywords"]:
                            keywords.append(i)
                        item["keywords"] = keywords
            with open(CONFIG, "w") as f:
                json.dump(data, f, indent=1)
            await ctx.send(embed=CreateAddEmbed(arguments))


@client.command()
async def start(ctx):
    author = ctx.message.author
    if author == 344400439728668672:
        while True:
            try:
                SearchMain()
                asyncio.wait(60)
            except:
                """"""


@client.command()
async def alerts(ctx):
    author = ctx.message.author
    with open(CONFIG, "r") as f:
        data = json.load(f)
    for item in data["configs"]:
        if item["id"] == str(author.id):
            if item["keywords"] == []:
                await ctx.send(embed=CreateNoAlertsEmbed())
            else:
                await ctx.send(embed=CreateAlertsEmbed(item))


@client.command()
async def removealert(ctx, *args):
    author = ctx.message.author
    with open(CONFIG, "r") as f:
        data = json.load(f)
        for item in data["configs"]:
            if item["id"] == str(author.id):
                keyword = " ".join(args)
                keywords = []
                remove = ""
                for i in item["keywords"]:
                    if keyword == i:
                        remove = i
                        await ctx.send(embed=CreateRemEmbed(remove))
                    keywords.append(i)
                if remove != "":
                    keywords.remove(remove)
                item["keywords"] = keywords
    with open(CONFIG, "w") as f:
        json.dump(data, f, indent=1)


@client.command()
async def addmonger(ctx, arg1):
    author = ctx.message.author
    if author.id == 344400439728668672:
        id = arg1
        with open(CONFIG, "r") as f:
            data = json.load(f)
            obj = {
                "id": id,
                "keywords": [],
            }
            configs = []
            configs.append(obj)
            for item in data["configs"]:
                configs.append(item)
            data["configs"] = configs
        with open(CONFIG, "w") as f:
            json.dump(data, f, indent=1)


@client.command()
async def clearalerts(ctx):
    author = ctx.message.author
    with open(CONFIG, "r") as f:
        data = json.load(f)
        for item in data["configs"]:
            if item["id"] == str(author.id):
                item["keywords"] = []
                await ctx.send(embed=CreateClearEmbed())
    with open(CONFIG, "w") as f:
        json.dump(data, f, indent=1)


if __name__ == "__main__":
    client.run(
        "MTAxMjgwMzYwMzU2MTQ0NzU3NQ.GnNbwC.ioF4DFJWju4fVJ_3ztbQNH0OCWmp_lH_Gnlprk"
    )
