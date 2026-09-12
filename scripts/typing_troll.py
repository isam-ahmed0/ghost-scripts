import asyncio
import random


@ghost.command(name="typingtroll", description="Show typing indicator for a long time, then do nothing.", usage="[@user]")
async def typingtroll(ctx, member: discord.Member = None):
    if member is None:
        await ctx.send("Mention someone: `.typingtroll @user`")
        return

    duration = random.randint(10, 30)
    await ctx.send(f"Typing to {member.mention}...")

    async with ctx.typing():
        await asyncio.sleep(duration)

    responses = [
        "nvm",
        "...",
        "nevermind",
        "I forgot what I was gonna say",
        "jk",
        "nmw",
        "actually nevermind",
        "lol nvm",
    ]
    await ctx.send(random.choice(responses))
