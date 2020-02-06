from utils.embed import Embed


def get_avatar_url(d_url):
    if "?" in d_url:
        d_url = d_url.split("?")[0]
        if ".webp" in d_url:
            d_url = d_url.replace(".webp", ".png")
    return d_url


async def send_help(ctx):
    subcmds = ctx.command.commands
    title = ctx.invoked_with
    author = {"name": ctx.bot.user.name, "icon_url": ctx.bot.user.avatar_url}
    desc = ctx.command.help
    fields = []
    for cmd in subcmds:
        fields.append([cmd.name, cmd.help, False])
    emb = Embed().make_emb(title, desc, author, fields)
    await ctx.send(embed=emb)
