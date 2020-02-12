from discord.ext import commands
import asyncio
import discord.utils
from utils.checks import check_create_logging, is_guild_admin, check_logging
from utils.embed import Embed
from utils.funx import send_help
import json


class Log(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.events = ["message_delete", "bulk_message_delete", "member_join", "member_remove", "member_ban", "member_unban"]

    @commands.group(aliases=["logs"])
    async def log(self, ctx):
        """Follow logging of certain events in your server."""
        if ctx.invoked_subcommand is None:
            await send_help(ctx)

    @is_guild_admin()
    @log.command()
    async def enable(self, ctx):
        """Enables log reports in a certain channel."""
        title = ctx.command.qualified_name
        author = {"name": ctx.bot.user.name, "icon_url": ctx.bot.user.avatar_url}
        desc = "I see you want to enable log reports in your server.\n To start, type the name or id of the channel in which you want the reports to be sent in. (30 secs)"
        fields = [["Examples", "`#channel_name` or\n`123456789123456789`", False]]
        en_embed = await ctx.send(embed=Embed().make_emb(title, desc, author, fields))

        def mess_check(m):
            return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id

        try:
            resp = await self.bot.wait_for("message", check=mess_check, timeout=30)
        except asyncio.TimeoutError:
            await ctx.send("You replied too late!", delete_after=5)
        else:
            if resp.content:
                chan_choice = None
                if "#" in resp.content:
                    chan_choice = discord.utils.get(ctx.guild.channels, mention=resp.content)
                elif resp.content.isdigit():
                    chan_choice = self.bot.get_channel(resp.content)
                if not chan_choice:
                    return await ctx.send("You didn't give me a valid channel!\nExamples: `#channel_name` or `123456789123456789`", delete_after=5)
                if not check_logging(ctx.guild.id):
                    check_create_logging(ctx.guild.id, chan_choice.id)
                    await ctx.send(f"Logging is now enabled and reports will be sent in {chan_choice.mention}!")
                else:
                    with open(f"data/guilds/{ctx.guild.id}/logging.json") as f:
                        data = json.load(f)
                    prev_chan_id = int(data["channel_id"])
                    if chan_choice.id == prev_chan_id:
                        return await ctx.send(f"Sorry, but logging is already enabled in {chan_choice.mention}.")
                    prev_chan = self.bot.get_channel(prev_chan_id)
                    r_text = f"Logging was previously disabled. Enable logging and change the logging channel to {chan_choice.mention}?"
                    if prev_chan:
                        r_text = f"Reports were previously sent in {prev_chan.mention}. Change the logging channel to {chan_choice.mention}?"
                    r_mess = await ctx.send(r_text)
                    expect_reacts = ["🆗", "❌"]

                    def reaction_check(reaction, user):
                        return user == ctx.author and str(reaction.emoji) in expect_reacts

                    for r in expect_reacts:
                        await r_mess.add_reaction(r)
                    try:
                        reaction, user = await self.bot.wait_for('reaction_add', timeout=10, check=reaction_check)
                    except asyncio.TimeoutError:
                        await ctx.send("I'll take this as a no...", delete_after=5)
                    else:
                        if str(reaction) == "❌":
                            await ctx.send("Ok! Nevermind, then.", delete_after=5)
                        elif str(reaction) == "🆗":
                            data["channel_id"] = chan_choice.id
                            with open(f"data/guilds/{ctx.guild.id}/logging.json", "w") as f:
                                json.dump(data, f)
                            await ctx.send(f"Logging is now enabled and reports will be sent in {chan_choice.mention}!")
                    finally:
                        await r_mess.delete()
                await en_embed.delete()

    @is_guild_admin()
    @log.command()
    async def disable(self, ctx):
        """Disables log reports in a certain channel."""
        r_mess = await ctx.send(f"I see you want to disable logging. Stop sending log reports?")
        expect_reacts = ["🆗", "❌"]

        def reaction_check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in expect_reacts

        for r in expect_reacts:
            await r_mess.add_reaction(r)
        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=10, check=reaction_check)
        except asyncio.TimeoutError:
            await ctx.send("I'll take this as a no...", delete_after=5)
        else:
            if str(reaction) == "❌":
                await ctx.send("Ok! Nevermind, then.", delete_after=5)
            elif str(reaction) == "🆗":
                if not check_logging(ctx.guild.id):
                    check_create_logging(ctx.guild.id, 0)
                else:
                    with open(f"data/guilds/{ctx.guild.id}/logging.json") as f:
                        data = json.load(f)
                    if int(data["channel_id"]) == 0:
                        return await ctx.send("Sorry, but logging is already disabled in this server")
                    data["channel_id"] = 0
                    with open(f"data/guilds/{ctx.guild.id}/logging.json", "w") as f:
                        json.dump(data, f)
                await ctx.send(f"Logging is now disabled. You won't be getting any more reports!")
        finally:
            await r_mess.delete()

    @log.command(aliases=["status"])
    async def stats(self, ctx):
        """See the logging configuration."""
        title = ctx.command.qualified_name
        author = {"name": ctx.bot.user.name, "icon_url": ctx.bot.user.avatar_url}
        desc = "You can see your configuration below:"
        enabled = "No"
        channel = "None"
        if check_logging(ctx.guild.id):
            with open(f"data/guilds/{ctx.guild.id}/logging.json") as f:
                data = json.load(f)
            set_chan = int(data["channel_id"])
            if not set_chan == 0:
                enabled = "Yes"
                channel = self.bot.get_channel(set_chan).mention
        events_disabled = data["events_disabled"]
        active_events = "None"
        inactive_events = "None"
        if events_disabled:
            inactive_events = "\n".join(events_disabled)
        act_ev_list = list()
        for ev in self.events:
            if not ev in events_disabled:
                act_ev_list.append(ev)
        if act_ev_list:
            active_events = "\n".join(act_ev_list)
        fields = [["Enabled", enabled, True], ["Channel", channel, True], ["Enabled events", active_events, False], ["Disabled events", inactive_events, False]]
        await ctx.send(embed=Embed().make_emb(title, desc, author, fields),)


def setup(bot):
    bot.add_cog(Log(bot))
