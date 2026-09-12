import asyncio
import time

reminders = {}


def parse_time(time_str):
    time_str = time_str.strip().lower()
    total_seconds = 0
    current = ""
    for char in time_str:
        if char.isdigit() or char == ".":
            current += char
        elif char in ("s", "m", "h", "d"):
            if not current:
                continue
            val = float(current)
            if char == "s":
                total_seconds += val
            elif char == "m":
                total_seconds += val * 60
            elif char == "h":
                total_seconds += val * 3600
            elif char == "d":
                total_seconds += val * 86400
            current = ""
    if current:
        total_seconds += float(current) * 60
    return int(total_seconds)


@ghost.command(name="remind", description="Set a reminder. Usage: .remind [time] [message]", usage="[time] [message]")
async def remind(ctx, time_str=None, *, message=None):
    if not time_str or not message:
        await ctx.send("Usage: `.remind 30m Check the oven` or `.remind 2h Meeting time`")
        return

    seconds = parse_time(time_str)
    if seconds <= 0 or seconds > 604800:
        await ctx.send("Time must be between 1s and 7d.")
        return

    remind_at = time.time() + seconds
    user_id = ctx.author.id

    if user_id not in reminders:
        reminders[user_id] = []

    reminders[user_id].append({"message": message, "at": remind_at, "channel": ctx.channel.id})

    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    time_parts = []
    if h:
        time_parts.append(f"{h}h")
    if m:
        time_parts.append(f"{m}m")
    if s:
        time_parts.append(f"{s}s")
    time_display = " ".join(time_parts) if time_parts else "0s"

    await ctx.send(f"Reminder set for **{time_display}** from now: `{message}`")
    asyncio.create_task(send_reminder(user_id, seconds, message))


async def send_reminder(user_id, seconds, message):
    await asyncio.sleep(seconds)
    if user_id in reminders:
        reminders[user_id] = [r for r in reminders[user_id] if r["message"] != message]
        if not reminders[user_id]:
            del reminders[user_id]
    try:
        user = await ghost.fetch_user(user_id)
        await user.send(f"**Reminder:** {message}")
    except Exception:
        pass


@ghost.command(name="reminders", description="View your pending reminders.", usage="")
async def reminders_cmd(ctx):
    user_id = ctx.author.id
    if user_id not in reminders or not reminders[user_id]:
        await ctx.send("You have no pending reminders.")
        return
    lines = []
    for i, r in enumerate(reminders[user_id], 1):
        remaining = int(r["at"] - time.time())
        if remaining <= 0:
            continue
        h = remaining // 3600
        m = (remaining % 3600) // 60
        s = remaining % 60
        parts = []
        if h:
            parts.append(f"{h}h")
        if m:
            parts.append(f"{m}m")
        if s:
            parts.append(f"{s}s")
        lines.append(f"  {i}. [{':'.join(parts) if parts else '0s'}] {r['message']}")
    if not lines:
        await ctx.send("You have no pending reminders.")
        return
    await ctx.send(f"```\nReminders:\n{chr(10).join(lines)}\n```")
