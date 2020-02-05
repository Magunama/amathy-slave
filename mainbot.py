import discord
from discord.ext import commands
import json
import itertools
from utils.embed import Embed
from os import listdir
from utils.checks import check_logging_enabled


def get_prefix(bot, message):
    fullpref = list()
    prefixes = ["c"]
    for k in prefixes:
        fullpref.extend(map(''.join, itertools.product(*zip(k.upper(), k.lower()))))
    return commands.when_mentioned_or(*fullpref)(bot, message)


def attach_cogs(bot):
    cog_blacklist = []
    cog_list = listdir("cogs/")
    for extension in cog_list:
        if not ".py" in extension:
            continue
        extension = extension[:-3]
        if not extension in cog_blacklist:
            try:
                bot.load_extension(f"cogs.{extension}")
                print(f"{extension}", end="; ")
            except discord.ext.commands.errors.ExtensionAlreadyLoaded:
                return
            except Exception as e:
                print()
                print(f"[ERR] Failed to load extension {extension}. Reason: {e}")


bot = commands.AutoShardedBot(command_prefix=get_prefix, fetch_offline_members=False, max_messages=1000)
# bot.remove_command('help')


@bot.event
async def on_ready():
    print('[INFO] Using account {} with id {}'.format(bot.user.name, bot.user.id))
    print("[INFO] Using discord.py version " + str(discord.__version__))
    print("Loaded plugins: ", end="")
    attach_cogs(bot)
    print()
    print(">>> Ready to play!")


@bot.event
async def on_shard_ready(shard):
    info = "\u001b[0m[\u001b[32;1mINFO\u001b[0m]"
    print(f'{info} Shard number {shard} is ready.')


@bot.event
async def on_raw_message_delete(payload):
    # Payload consists of RawMessageDeleteEvent

    dest_id = check_logging_enabled(payload)
    if dest_id == 0:
        return
    payload.bot_user = bot.user
    dest_chan = bot.get_channel(dest_id)
    embs = Embed().message_delete(payload)
    for e in embs:
        await dest_chan.send(embed=e)


@bot.event
async def on_raw_bulk_message_delete(payload):
    # Payload consists of RawBulkMessageDeleteEvent

    dest_id = check_logging_enabled(payload)
    if dest_id == 0:
        return
    payload.bot_user = bot.user
    dest_chan = bot.get_channel(dest_id)
    embs = Embed().bulk_message_delete(payload)
    for e in embs:
        await dest_chan.send(embed=e)


@bot.event
async def on_raw_message_edit(payload):
    pass
