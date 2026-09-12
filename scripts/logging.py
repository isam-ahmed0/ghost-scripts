import os
from datetime import datetime

PREFIX = ghost.command_prefix

LOG_DIR = os.path.join(files.get_application_support(), "logs")
os.makedirs(LOG_DIR, exist_ok=True)


def _timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _append(path, line):
    with open(path, "a", encoding="utf-8") as f:
        f.write(line)


def _read_tail(path, lines_count):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    content = "".join(lines[-lines_count:])
    if len(content) > 1900:
        content = content[-1900:]
    return content


# ─────────────────────────────────────────────
#  DM logger
# ─────────────────────────────────────────────

DM_LOG_PATH = os.path.join(LOG_DIR, "dm_log.txt")


async def handle_dm_message(message):
    if message.guild is not None:
        return
    if message.author.id == ghost.user.id or message.author.bot:
        return
    line = f"[{_timestamp()}] {message.author} ({message.author.id}): {message.content or '[no text content]'}\n"
    _append(DM_LOG_PATH, line)


ghost.add_listener(handle_dm_message, "message")


@ghost.command(name="dms", description="Show last 10 logged DMs.", usage="")
async def dms(ctx):
    content = _read_tail(DM_LOG_PATH, 10)
    if not content.strip():
        await ctx.send("No DMs logged yet.")
        return
    await ctx.send(f"```\nLast DMs:\n{content}\n```")


@ghost.command(name="dmsearch", description="Search DM logs.", usage="[query]")
async def dmsearch(ctx, *, query=None):
    if not query:
        await ctx.send(f"Usage: `{PREFIX}dmsearch [keyword]`")
        return
    if not os.path.exists(DM_LOG_PATH):
        await ctx.send("No DMs logged yet.")
        return
    with open(DM_LOG_PATH, "r", encoding="utf-8") as f:
        matches = [l for l in f.readlines() if query.lower() in l.lower()]
    if not matches:
        await ctx.send(f"No DMs matching `{query}`.")
        return
    content = "".join(matches[-10:])
    if len(content) > 1900:
        content = content[-1900:]
    await ctx.send(f"```\nDMs matching '{query}':\n{content}\n```")


@ghost.command(name="dmclear", description="Clear DM log.", usage="")
async def dmclear(ctx):
    with open(DM_LOG_PATH, "w", encoding="utf-8") as f:
        f.write("")
    await ctx.send("DM log cleared.")


# ─────────────────────────────────────────────
#  Ping monitor
# ─────────────────────────────────────────────

PING_LOG_PATH = os.path.join(LOG_DIR, "ping_log.txt")
ping_entries = []


async def handle_ping(message):
    if message.guild is None:
        return
    if ghost.user not in message.mentions:
        return
    entry = {
        "time": _timestamp(),
        "channel": str(message.channel),
        "author": str(message.author),
        "content": message.content or "[no text content]",
    }
    ping_entries.append(entry)
    if len(ping_entries) > 100:
        ping_entries.pop(0)
    line = f"[{entry['time']}] #{message.channel} by {message.author}: {message.content or '[no text]'}\n"
    _append(PING_LOG_PATH, line)


ghost.add_listener(handle_ping, "message")


@ghost.command(name="pinglog", description="Show last 10 pings you received.", usage="")
async def pinglog(ctx):
    if not ping_entries:
        await ctx.send("No pings recorded yet.")
        return
    lines = []
    for p in ping_entries[-10:]:
        lines.append(f"  [{p['time']}] #{p['channel']} by {p['author']}: {p['content'][:60]}")
    await ctx.send(f"```\nRecent pings:\n{chr(10).join(lines)}\n```")


@ghost.command(name="pingclear", description="Clear ping log.", usage="")
async def pingclear(ctx):
    ping_entries.clear()
    if os.path.exists(PING_LOG_PATH):
        os.remove(PING_LOG_PATH)
    await ctx.send("Ping log cleared.")


# ─────────────────────────────────────────────
#  Channel message logger
# ─────────────────────────────────────────────

logged_channels = set()


async def handle_channel_log(message):
    if message.guild is None or message.author.id == ghost.user.id:
        return
    if message.channel.id not in logged_channels:
        return
    content = message.content or "[no text content]"
    if message.attachments:
        content += " [attachments: " + ", ".join(a.url for a in message.attachments) + "]"
    line = f"[{_timestamp()}] {message.author}: {content}\n"
    _append(os.path.join(LOG_DIR, f"channel_{message.channel.id}.txt"), line)


ghost.add_listener(handle_channel_log, "message")


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


# ─────────────────────────────────────────────
#  Stats tracker
# ─────────────────────────────────────────────

user_stats = {}
guild_stats = {}


async def handle_stats(message):
    if message.guild is None:
        return
    uid = message.author.id
    cid = message.channel.id
    gid = message.guild.id

    if uid not in user_stats:
        user_stats[uid] = {"total": 0, "channels": {}, "guilds": {}}
    user_stats[uid]["total"] += 1
    user_stats[uid]["channels"][cid] = user_stats[uid]["channels"].get(cid, 0) + 1
    user_stats[uid]["guilds"][gid] = user_stats[uid]["guilds"].get(gid, 0) + 1
    guild_stats[gid] = guild_stats.get(gid, 0) + 1


ghost.add_listener(handle_stats, "message")


@ghost.command(name="mystats", description="View your message stats.", usage="")
async def mystats(ctx):
    uid = ctx.author.id
    if uid not in user_stats:
        await ctx.send("No stats recorded for you yet.")
        return

    stats = user_stats[uid]
    top_channel = max(stats["channels"], key=stats["channels"].get) if stats["channels"] else None
    top_ch_obj = ctx.guild.get_channel(top_channel) if top_channel else None
    top_ch_name = top_ch_obj.name if top_ch_obj else "N/A"
    top_ch_count = stats["channels"].get(top_channel, 0) if top_channel else 0
    rank = sorted(user_stats.keys(), key=lambda x: user_stats[x]["total"], reverse=True).index(uid) + 1

    await ctx.send(
        f"```\nStats for {ctx.author.display_name}:\n"
        f"  Total messages: {stats['total']}\n"
        f"  Server rank: #{rank}\n"
        f"  Most active channel: #{top_ch_name} ({top_ch_count})\n"
        f"  Servers active in: {len(stats['guilds'])}\n```"
    )


@ghost.command(name="serverstats", description="View server message stats.", usage="")
async def serverstats(ctx):
    if not guild_stats:
        await ctx.send("No stats recorded yet.")
        return

    gid = ctx.guild.id
    total = guild_stats.get(gid, 0)
    server_users = {uid: s for uid, s in user_stats.items() if gid in s.get("guilds", {})}
    top_users = sorted(server_users.items(), key=lambda x: x[1]["guilds"].get(gid, 0), reverse=True)[:5]

    lines = [f"  Total messages: {total}", f"  Active users: {len(server_users)}", "", "  Top 5 users:"]
    for i, (uid, s) in enumerate(top_users, 1):
        member = ctx.guild.get_member(uid)
        name = member.display_name if member else str(uid)
        lines.append(f"    {i}. {name}: {s['guilds'].get(gid, 0)}")

    await ctx.send(f"```\nServer Stats ({ctx.guild.name}):\n{chr(10).join(lines)}\n```")