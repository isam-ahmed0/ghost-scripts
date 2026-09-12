import os
from datetime import datetime

ping_log_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ping_log.txt")
ping_entries = []


async def on_message(message):
    if message.guild is None:
        return
    if ghost.user in message.mentions:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = {
            "time": timestamp,
            "channel": str(message.channel),
            "guild": str(message.guild),
            "author": str(message.author),
            "content": message.content or "[no text content]"
        }
        ping_entries.append(entry)
        if len(ping_entries) > 100:
            ping_entries.pop(0)

        line = f"[{timestamp}] #{message.channel} by {message.author}: {message.content or '[no text]'}\n"
        with open(ping_log_path, "a", encoding="utf-8") as f:
            f.write(line)


@ghost.command(name="pinglog", description="Show last 10 pings you received.", usage="")
async def pinglog(ctx):
    if not ping_entries:
        await ctx.send("No pings recorded yet.")
        return
    recent = ping_entries[-10:]
    lines = []
    for p in recent:
        lines.append(f"  [{p['time']}] #{p['channel']} by {p['author']}: {p['content'][:60]}")
    await ctx.send(f"```\nRecent pings:\n{chr(10).join(lines)}\n```")


@ghost.command(name="pingclear", description="Clear ping log.", usage="")
async def pingclear(ctx):
    ping_entries.clear()
    if os.path.exists(ping_log_path):
        with open(ping_log_path, "w", encoding="utf-8") as f:
            f.write("")
    await ctx.send("Ping log cleared.")
