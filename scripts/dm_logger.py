import os
from datetime import datetime

dm_log_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dm_log.txt")


def log_dm(author, content, author_id):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {author} ({author_id}): {content}\n"
    with open(dm_log_path, "a", encoding="utf-8") as f:
        f.write(entry)


async def on_message(message):
    if message.guild is not None:
        return
    if message.author.id == ghost.user.id:
        return
    if message.author.bot:
        return
    log_dm(str(message.author), message.content or "[no text content]", message.author.id)


@ghost.command(name="dms", description="Show last 10 logged DMs.", usage="")
async def dms(ctx):
    if not os.path.exists(dm_log_path):
        await ctx.send("No DMs logged yet.")
        return
    with open(dm_log_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    if not lines:
        await ctx.send("No DMs logged yet.")
        return
    recent = lines[-10:]
    content = "".join(recent)
    if len(content) > 1900:
        content = content[-1900:]
    await ctx.send(f"```\nLast DMs:\n{content}\n```")


@ghost.command(name="dmsearch", description="Search DM logs.", usage="[query]")
async def dmsearch(ctx, *, query=None):
    if not query:
        await ctx.send("Usage: `.dmsearch [keyword]`")
        return
    if not os.path.exists(dm_log_path):
        await ctx.send("No DMs logged yet.")
        return
    with open(dm_log_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    matches = [l for l in lines if query.lower() in l.lower()]
    if not matches:
        await ctx.send(f"No DMs matching `{query}`.")
        return
    recent = matches[-10:]
    content = "".join(recent)
    if len(content) > 1900:
        content = content[-1900:]
    await ctx.send(f"```\nDMs matching '{query}':\n{content}\n```")


@ghost.command(name="dmclear", description="Clear DM log.", usage="")
async def dmclear(ctx):
    if os.path.exists(dm_log_path):
        with open(dm_log_path, "w", encoding="utf-8") as f:
            f.write("")
    await ctx.send("DM log cleared.")
