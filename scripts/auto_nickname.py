from discord.ext import tasks

nick_names = []
nick_index = 0
nick_loop = None
nick_guild_id = None


@ghost.command(name="autonick", description="Rotate nicknames. Usage: .autonick [name1] [name2] ... [interval]", usage="[names] [interval]")
async def autonick(ctx, *, args=None):
    global nick_names, nick_index, nick_loop, nick_guild_id

    if not args:
        await ctx.send(
            "```\n"
            "Auto Nickname Commands:\n"
            "  .autonick Name1 Name2 Name3  - Set nicknames to rotate\n"
            "  .autonick stop               - Stop rotation\n"
            "```"
        )
        return

    if args.lower() == "stop":
        if nick_loop and nick_loop.is_running():
            nick_loop.cancel()
            nick_loop = None
            await ctx.send("Auto nickname stopped.")
        else:
            await ctx.send("Auto nickname is not running.")
        return

    parts = args.split()
    interval = 300
    names = []
    for p in parts:
        try:
            val = int(p)
            if val >= 30:
                interval = val
            else:
                names.append(p)
        except ValueError:
            names.append(p)

    if not names:
        await ctx.send("Provide at least one nickname: `.autonick Ghost Phantom Specter`")
        return

    nick_names = names
    nick_index = 0
    nick_guild_id = ctx.guild.id

    if nick_loop and nick_loop.is_running():
        nick_loop.cancel()

    nick_loop = tasks.loop(seconds=interval)(rotate_nickname)
    nick_loop.start()
    await ctx.send(f"Auto nickname started ({interval}s, {len(names)} names)")


async def rotate_nickname():
    global nick_index
    if not nick_names or not nick_guild_id:
        return
    try:
        guild = ghost.get_guild(nick_guild_id)
        if guild:
            me = guild.get_member(ghost.user.id)
            if me:
                await me.edit(nick=nick_names[nick_index % len(nick_names)])
                nick_index += 1
    except Exception:
        pass
