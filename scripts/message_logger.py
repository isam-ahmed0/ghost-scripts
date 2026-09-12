import os
from datetime import datetime

logged_channels = set()
log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "channel_logs")
os.makedirs(log_dir, exist_ok=True)


async def on_message(message):
    if message.guild is None:
        return
    if message.author.id == ghost.user.id:
        return
    if message.channel.id not in logged_channels:
        return
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    author = str(message.author)
    content = message.content or "[no text content]"
    attachments = ", ".join(a.url for a in message.attachments) if message.attachments else ""
    log_file = os.path.join(log_dir, f"{message.channel.id}.txt")
    entry = f"[{timestamp}] {author}: {content}"
    if attachments:
        entry += f" [attachments: {attachments}]"
    entry += "\n"
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(entry)


@ghost.command(name="logchannel", description="Start logging a channel.", usage="#channel")
async def logchannel(ctx, channel: discord.TextChannel = None):
    if not channel:
        channel = ctx.channel
    logged_channels.add(channel.id)
    await ctx.send(f"Now logging {channel.mention}")


@ghost.command(name="logstop", description="Stop logging a channel.", usage="#channel")
async def logstop(ctx, channel: discord.TextChannel = None):
    if not channel:
        channel = ctx.channel
    logged_channels.discard(channel.id)
    await ctx.send(f"Stopped logging {channel.mention}")


@ghost.command(name="logstatus", description="Show which channels are being logged.", usage="")
async def logstatus(ctx):
    if not logged_channels:
        await ctx.send("No channels are being logged.")
        return
    lines = []
    for cid in logged_channels:
        ch = ghost.get_channel(cid)
        lines.append(f"  - {ch.mention if ch else cid}")
    await ctx.send(f"```\nLogged channels:\n{chr(10).join(lines)}\n```")
