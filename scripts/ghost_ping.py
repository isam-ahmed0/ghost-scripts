import asyncio


@ghost.command(name="ghostping", description="Send a fake ghost ping that auto-deletes.", usage="[@user]")
async def ghostping(ctx, member: discord.Member = None):
    if member is None:
        await ctx.send("Mention someone: `.ghostping @user`")
        return

    msg = await ctx.send(f"**BOO!** {member.mention}")
    await asyncio.sleep(1)
    try:
        await msg.delete()
    except Exception:
        pass

    try:
        await ctx.message.delete()
    except Exception:
        pass
