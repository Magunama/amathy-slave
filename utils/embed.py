import discord
import random
import datetime
import json


class Embed:
    def __init__(self):
        self.colors = [0x004080, 0x008080, 0xff8040, 0xff0000, 0x804040, 0x400000, 0x004000, 0x008080, 0x004080,
                       0x8000ff, 0xff00ff, 0x800040, 0x000040]

    def color_list(self):
        return self.colors

    def make_emb(self, title, desc, author, fields, footer=None, url=None, timestamp=None, empty_field=False):
        embed = discord.Embed(title=title, description=desc, color=random.choice(self.color_list()), url=url)
        embed.set_author(name=author["name"], icon_url=author["icon_url"])
        for field in fields:
            name = field[0]
            value = field[1]

            if empty_field:
                if not name:
                    name = "\u200b"
                if not value:
                    value = "\u200b"

            inline = field[2]
            if not inline:
                inline = True
            if name and value:
                embed.add_field(name=name, value=value, inline=inline)
        if not timestamp:
            timestamp = datetime.datetime.utcnow()
        embed.timestamp = timestamp
        if not footer:
            footer = ">>> Please donate to my master Amathy <<<"
        embed.set_footer(text=footer)
        return embed

    def message_delete(self, payload):
        chan_id = payload.channel_id
        mess_id = payload.message_id

        desc = f"A message sent in channel with id {chan_id} was deleted."
        fields = [[None, None, None]]
        if hasattr(payload, "cached_message"):
            cached_mess = payload.cached_message
            if hasattr(cached_mess, "author"):
                author = cached_mess.author
                if author.bot:
                    return []
                chan_mention = cached_mess.channel.mention
                desc = f"A message sent by `{author}` in {chan_mention} was deleted."
                fields = [["Content", cached_mess.content[:1000], None]]
        title = "Reporting for duty!"
        footer = f"Message id: {mess_id}"
        embed_author = {"name": payload.bot_user.name, "icon_url": payload.bot_user.avatar_url}
        return [self.make_emb(title, desc, embed_author, fields, footer)]

    def bulk_message_delete(self, payload):
        chan_id = payload.channel_id
        cached_messages = payload.cached_messages
        mess_count = len(cached_messages)

        title = "Reporting for duty!"
        author = {"name": payload.bot_user.name, "icon_url": payload.bot_user.avatar_url}
        desc = f"{mess_count} sent in channel with id {chan_id} were deleted."
        fields = [[None, None, None]]
        if not cached_messages:
            return [self.make_emb(title, desc, author, fields)]
        embeds = []
        for mess in cached_messages:
            if hasattr(mess, "author"):
                if not mess.author.bot:
                    chan_mention = mess.channel.mention
                    desc = f"A message sent by `{mess.author}` in {chan_mention} was deleted."
                    fields = [["Content", mess.content[:1000], None]]
                    footer = f"Message id: {mess.id}"
                    embeds.append(self.make_emb(title, desc, author, fields, footer))
        return embeds

    def message_edit(self, bot, payload):
        message_id = payload.message_id
        chan_obj = bot.get_channel(payload.channel_id)
        data = payload.data
        after_cont = data["content"]
        mess_author = data["author"]["username"] + "#" + data["author"]["discriminator"]
        title = "Reporting for duty!"
        author = {"name": bot.user.name, "icon_url": bot.user.avatar_url}
        desc = f"`{mess_author}` edited their message in {chan_obj.mention}"
        footer = f"Message id: {message_id}"
        fields = [["After message", after_cont, False]]
        cached_mess = payload.cached_message
        if hasattr(cached_mess, "content"):
            before_cont = cached_mess.content
            fields.insert(0, ["Before message", before_cont, False])
        return [self.make_emb(title, desc, author, fields, footer)]

    def member_join_left(self, bot, member, action):
        title = "Reporting for duty!"
        author = {"name": bot.user.name, "icon_url": bot.user.avatar_url}
        desc = f"`{member}` just {action} the server."
        footer = f"Member id: {member.id}"
        fields = [[None, None, None]]
        return [self.make_emb(title, desc, author, fields, footer)]

    def member_ban_unban(self, bot, entry):
        action = entry.action.name
        title = "Reporting for duty!"
        author = {"name": bot.user.name, "icon_url": bot.user.avatar_url}
        desc = f"Action `{action}` with id: `{entry.id}`"
        fields = [[f"User that got {action}ned", entry.target, False], [f"User who initiated the {action}", entry.user, False]]
        if hasattr(entry, "reason"):
            fields.append([f"Reason of the {entry.action}", entry.reason, False])
        return [self.make_emb(title, desc, author, fields)]
