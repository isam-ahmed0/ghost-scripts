import asyncio
import time

PREFIX = ghost.command_prefix


# ─────────────────────────────────────────────
#  Auto status rotation
# ─────────────────────────────────────────────

statuses = []
status_index = 0
status_loop = None


@ghost.command(name="autostatus", description="Manage auto status rotation.", usage="[add|remove|list|start|stop] [text]")
async def autostatus(ctx, action=None, *, text=None):
    global status_index, status_loop

    if action is None:
        await ctx.send(
            "```\n"
            "Auto Status Commands:\n"
            f"  {PREFIX}autostatus add [text]    - Add a status\n"
            f"  {PREFIX}autostatus remove [num]  - Remove status by number\n"
            f"  {PREFIX}autostatus list          - List all statuses\n"
            f"  {PREFIX}autostatus start [sec]   - Start rotation (default 60s)\n"
            f"  {PREFIX}autostatus stop          - Stop rotation\n"
            "```"
        )
        return

    action = action.lower()

    if action == "add":
        if not text:
            await ctx.send(f"Provide status text: `{PREFIX}autostatus add Playing with ghosts`")
            return
        statuses.append(text)
        await ctx.send(f"Added status #{len(statuses)}: `{text}`")

    elif action == "remove":
        if not text:
            await ctx.send(f"Provide status number: `{PREFIX}autostatus remove 1`")
            return
        try:
            removed = statuses.pop(int(text) - 1)
            await ctx.send(f"Removed: `{removed}`")
        except (ValueError, IndexError):
            await ctx.send("Invalid status number.")

    elif action == "list":
        if not statuses:
            await ctx.send(f"No statuses configured. Use `{PREFIX}autostatus add [text]` to add one.")
            return
        listing = "\n".join(f"  {i + 1}. {s}" for i, s in enumerate(statuses))
        await ctx.send(f"```\nStatuses:\n{listing}\n```")

    elif action == "start":
        if not statuses:
            await ctx.send(f"Add statuses first with `{PREFIX}autostatus add [text]`")
            return
        interval = 60
        if text:
            try:
                interval = int(text)
            except ValueError:
                interval = 60
        if status_loop and status_loop.is_running():
            status_loop.cancel()
        status_loop = tasks.loop(seconds=interval)(rotate_status)
        status_loop.start()
        await ctx.send(f"Auto status started ({interval}s interval, {len(statuses)} statuses)")

    elif action == "stop":
        if status_loop and status_loop.is_running():
            status_loop.cancel()
            status_loop = None
            await ctx.send("Auto status stopped.")
        else:
            await ctx.send("Auto status is not running.")


async def rotate_status():
    global status_index
    if not statuses:
        return
    try:
        activity = discord.CustomActivity(name=statuses[status_index % len(statuses)])
        await ghost.change_presence(activity=activity)
        status_index += 1
    except Exception:
        pass


@ghost.command(name="statuslist", description="Quick alias for status list.", usage="")
async def statuslist(ctx):
    await autostatus(ctx, "list")


# ─────────────────────────────────────────────
#  Auto nickname rotation
# ─────────────────────────────────────────────

nick_names = []
nick_index = 0
nick_loop = None
nick_guild_id = None


@ghost.command(name="autonick", description="Rotate nicknames.", usage="[names] [interval]")
async def autonick(ctx, *, args=None):
    global nick_names, nick_index, nick_loop, nick_guild_id

    if not args:
        await ctx.send(
            "```\n"
            "Auto Nickname Commands:\n"
            f"  {PREFIX}autonick Name1 Name2 Name3  - Set nicknames to rotate\n"
            f"  {PREFIX}autonick stop               - Stop rotation\n"
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
        await ctx.send(f"Provide at least one nickname: `{PREFIX}autonick Ghost Phantom Specter`")
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


# ─────────────────────────────────────────────
#  Reminders
# ─────────────────────────────────────────────

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
            total_seconds += int(val * {"s": 1, "m": 60, "h": 3600, "d": 86400}[char])
            current = ""
    if current:
        total_seconds += int(float(current) * 60)
    return int(total_seconds)


def format_seconds(seconds):
    parts = []
    for unit, size in (("d", 86400), ("h", 3600), ("m", 60), ("s", 1)):
        if seconds >= size:
            parts.append(f"{seconds // size}{unit}")
            seconds %= size
    return " ".join(parts) if parts else "0s"


@ghost.command(name="remind", description="Set a reminder. Usage: .remind [time] [message]", usage="[time] [message]")
async def remind(ctx, time_str=None, *, message=None):
    if not time_str or not message:
        await ctx.send(f"Usage: `{PREFIX}remind 30m Check the oven` or `{PREFIX}remind 2h Meeting time`")
        return

    seconds = parse_time(time_str)
    if seconds <= 0 or seconds > 604800:
        await ctx.send("Time must be between 1s and 7d.")
        return

    user_id = ctx.author.id
    remind_at = time.time() + seconds

    if user_id not in reminders:
        reminders[user_id] = []
    reminders[user_id].append({"message": message, "at": remind_at})

    await ctx.send(f"Reminder set for **{format_seconds(seconds)}** from now: `{message}`")
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
        lines.append(f"  {i}. [{format_seconds(remaining)}] {r['message']}")

    if not lines:
        await ctx.send("You have no pending reminders.")
        return

    await ctx.send(f"```\nReminders:\n{chr(10).join(lines)}\n```")