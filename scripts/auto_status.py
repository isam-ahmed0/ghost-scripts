import asyncio
from discord.ext import tasks

statuses = []
status_index = 0
status_loop = None


@ghost.command(name="autostatus", description="Manage auto status rotation.", usage="[add|remove|list|start|stop] [text]")
async def autostatus(ctx, action=None, *, text=None):
    global statuses, status_index, status_loop

    if action is None:
        await ctx.send(
            "```\n"
            "Auto Status Commands:\n"
            "  .autostatus add [text]    - Add a status\n"
            "  .autostatus remove [num]  - Remove status by number\n"
            "  .autostatus list          - List all statuses\n"
            "  .autostatus start [sec]   - Start rotation (default 60s)\n"
            "  .autostatus stop          - Stop rotation\n"
            "```"
        )
        return

    if action.lower() == "add":
        if not text:
            await ctx.send("Provide status text: `.autostatus add Playing with ghosts`")
            return
        statuses.append(text)
        await ctx.send(f"Added status #{len(statuses)}: `{text}`")

    elif action.lower() == "remove":
        if not text:
            await ctx.send("Provide status number: `.autostatus remove 1`")
            return
        try:
            idx = int(text) - 1
            removed = statuses.pop(idx)
            await ctx.send(f"Removed: `{removed}`")
        except (ValueError, IndexError):
            await ctx.send("Invalid status number.")

    elif action.lower() == "list":
        if not statuses:
            await ctx.send("No statuses configured. Use `.autostatus add [text]` to add one.")
            return
        listing = "\n".join(f"  {i+1}. {s}" for i, s in enumerate(statuses))
        await ctx.send(f"```\nStatuses:\n{listing}\n```")

    elif action.lower() == "start":
        if not statuses:
            await ctx.send("Add statuses first with `.autostatus add [text]`")
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

    elif action.lower() == "stop":
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
