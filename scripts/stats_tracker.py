user_stats = {}
channel_stats = {}
guild_stats = {}


async def on_message(message):
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

    channel_stats[cid] = channel_stats.get(cid, 0) + 1
    guild_stats[gid] = guild_stats.get(gid, 0) + 1


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
        f"```\n"
        f"Stats for {ctx.author.display_name}:\n"
        f"  Total messages: {stats['total']}\n"
        f"  Server rank: #{rank}\n"
        f"  Most active channel: #{top_ch_name} ({top_ch_count})\n"
        f"  Servers active in: {len(stats['guilds'])}\n"
        f"```"
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
