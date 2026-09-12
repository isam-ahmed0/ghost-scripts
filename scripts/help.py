import os

PREFIX = ghost.command_prefix

NATIVE_COMMANDS = {
    "General": {
        "emoji": "📖",
        "commands": {
            f"{PREFIX}help": "A list of all categories",
            f"{PREFIX}ping": "Check the bot's latency",
            f"{PREFIX}search [query] [page]": "Search for commands",
        }
    },
    "Account": {
        "emoji": "👤",
        "commands": {
            f"{PREFIX}account": "Account commands",
            f"{PREFIX}backups": "List your backups",
            f"{PREFIX}backup": "Backup management",
            f"{PREFIX}hypesquad [house]": "Change your hypesquad",
            f"{PREFIX}status [status]": "Change your online status",
            f"{PREFIX}customstatus [status]": "Change your custom status",
            f"{PREFIX}clearstatus": "Clear your custom status",
            f"{PREFIX}playing [status]": "Set a playing status",
            f"{PREFIX}streaming [status]": "Set a streaming status",
            f"{PREFIX}nickname [name]": "Change your server nickname",
            f"{PREFIX}clearnickname": "Clear your nickname",
            f"{PREFIX}discordtheme [theme]": "Change Discord theme",
            f"{PREFIX}yoinkrpc [user]": "Steal someone's rich presence",
        }
    },
    "Fun": {
        "emoji": "🎉",
        "commands": {
            f"{PREFIX}rickroll": "Never gonna give you up",
            f"{PREFIX}coinflip": "Flip a coin",
            f"{PREFIX}iq [user]": "Get the IQ of a user",
            f"{PREFIX}howgay [user]": "Get the gayness of a user",
            f"{PREFIX}pp [user]": "Get the pp size",
            f"{PREFIX}rps": "Play rock paper scissors",
            f"{PREFIX}slots": "Play a slot machine",
            f"{PREFIX}encodemorsecode [text]": "Encode text to morse code",
            f"{PREFIX}blocksend [user] [msg]": "Send message to blocked user",
            f"{PREFIX}randomdata [type]": "Generate random data",
            f"{PREFIX}kanye": "Random Kanye quote",
            f"{PREFIX}socialcredit [user]": "Social credit score",
            f"{PREFIX}dice [sides]": "Roll a dice",
            f"{PREFIX}rainbow [text]": "Create rainbow text",
            f"{PREFIX}rainbowreact [msg id]": "Rainbow reaction",
            f"{PREFIX}dox [user]": "Dox a user (fake)",
            f"{PREFIX}meme": "Get a random meme",
            f"{PREFIX}dadjoke": "Get a dad joke",
            f"{PREFIX}insult": "Get a random insult",
            f"{PREFIX}compliment [user]": "Get a random compliment",
            f"{PREFIX}catfact": "Get a random cat fact",
            f"{PREFIX}yomomma": "Get a yo momma joke",
            f"{PREFIX}8ball [question]": "Ask the magic 8ball",
            f"{PREFIX}fakenitro": "Fake a nitro gift",
            f"{PREFIX}hyperlink [link] [text]": "Create a hyperlink",
            f"{PREFIX}aura [user]": "Check a user's aura",
            f"{PREFIX}gyatt [user]": "Check if they've got GYATTT",
            f"{PREFIX}playsound [url]": "Play a 5 second sound",
        }
    },
    "Text": {
        "emoji": "✏️",
        "commands": {
            f"{PREFIX}shrug": "Shrug your arms",
            f"{PREFIX}tableflip": "Flip the table",
            f"{PREFIX}unflip": "Put the table back",
            f"{PREFIX}lmgtfy [search]": "Let me Google that for you",
            f"{PREFIX}blank": "Send a blank message",
            f"{PREFIX}fakepurge": "Flood chat with blank messages",
            f"{PREFIX}ascii [text]": "Create ASCII text art",
            f"{PREFIX}aesthetic [text]": "Make text aesthetic",
            f"{PREFIX}chatbypass [text]": "Bypass chat filters",
            f"{PREFIX}regional [text]": "Text out of emojis",
            f"{PREFIX}randomcase [text]": "Random case text",
            f"{PREFIX}animate [text]": "Animate text",
            f"{PREFIX}cembed": "Custom embed builder",
            f"{PREFIX}passwordgen [length]": "Generate a password",
            f"{PREFIX}codeblock [lang] [code]": "Create a codeblock",
            f"{PREFIX}json / python / js / html / css": "Language codeblocks",
            f"{PREFIX}java / c / cpp / php / lua": "More codeblocks",
            f"{PREFIX}reverse [text]": "Reverse your text",
        }
    },
    "Util": {
        "emoji": "🧰",
        "commands": {
            f"{PREFIX}config": "View config (redacted)",
            f"{PREFIX}config set [key] [value]": "Set a config value",
            f"{PREFIX}restart": "Restart the bot",
            f"{PREFIX}quit": "Quit the bot",
            f"{PREFIX}settings": "View bot settings",
            f"{PREFIX}prefix [prefix]": "Change command prefix",
            f"{PREFIX}clearcache": "Clear the cache",
            f"{PREFIX}richpresence": "Toggle rich presence",
            f"{PREFIX}resetrichpresence": "Reset RPC to defaults",
            f"{PREFIX}specs": "View computer specs",
            f"{PREFIX}sessionspoofer [device]": "Spoof session device",
            f"{PREFIX}uptime": "View bot uptime",
            f"{PREFIX}latency": "Check bot latency",
            f"{PREFIX}allcmds": "Export all commands to file",
            f"{PREFIX}clearconsole": "Clear the console",
            f"{PREFIX}commandhistory": "Command usage history",
            f"{PREFIX}telemetry": "Toggle telemetry",
        }
    },
}

SCRIPT_CATEGORIES = {
    "Script Games": {
        "emoji": "🎮",
        "commands": {
            f"{PREFIX}adventure": "Start a dungeon adventure",
            f"{PREFIX}choice [1-3]": "Make a choice in adventure",
            f"{PREFIX}numbergame [easy|hard]": "Number guessing game",
            f"{PREFIX}num [number]": "Guess the number",
            f"{PREFIX}wordguess": "Start a hangman word game",
            f"{PREFIX}guess [letter]": "Guess a letter",
            f"{PREFIX}ttt @user": "Start Tic-Tac-Toe",
            f"{PREFIX}ttt [1-9]": "Place your mark",
            f"{PREFIX}trivia": "Play a trivia question",
            f"{PREFIX}triviascore": "View trivia leaderboard",
        }
    },
    "Script Fun": {
        "emoji": "🎲",
        "commands": {
            f"{PREFIX}fortune": "Get a random fortune told",
            f"{PREFIX}mock [text]": "mOcKiFy TeXt (spongebob case)",
            f"{PREFIX}mockify [text]": "Same as mock",
            f"{PREFIX}autocorrect [text]": "Correct words to food names",
            f"{PREFIX}ghostping @user": "Ghost ping that auto-deletes",
            f"{PREFIX}typingtroll @user": "Type for 10-30s then say nothing",
            f"{PREFIX}complimentbomb @user": "Send 3 compliments to someone",
        }
    },
    "Script Utility": {
        "emoji": "🔧",
        "commands": {
            f"{PREFIX}autostatus": "Rotate custom statuses on a timer",
            f"{PREFIX}statuslist": "Quick alias for status list",
            f"{PREFIX}autonick [names]": "Rotate nicknames on a timer",
            f"{PREFIX}remind [time] [msg]": "Set a reminder that DMs you",
            f"{PREFIX}reminders": "View your pending reminders",
        }
    },
    "Script Logging": {
        "emoji": "📁",
        "commands": {
            f"{PREFIX}dms": "Show last 10 logged DMs",
            f"{PREFIX}dmsearch [query]": "Search your DM log",
            f"{PREFIX}dmclear": "Clear DM log",
            f"{PREFIX}pinglog": "Show last 10 pings you received",
            f"{PREFIX}pingclear": "Clear ping log",
            f"{PREFIX}logchannel #chan": "Start logging a channel",
            f"{PREFIX}logstop #chan": "Stop logging a channel",
            f"{PREFIX}logstatus": "Show logged channels",
            f"{PREFIX}mystats": "View your message statistics",
            f"{PREFIX}serverstats": "View server-wide statistics",
        }
    },
    "Script Help": {
        "emoji": "📚",
        "commands": {
            f"{PREFIX}shelp [page]": "Show help for all command categories",
            f"{PREFIX}shelprange [start]-[end]": "Show multiple help pages",
            f"{PREFIX}scmds": "List all script commands",
            f"{PREFIX}ncmds": "List all native Ghost commands",
            f"{PREFIX}scripts": "List all loaded script files",
            f"{PREFIX}cmds [query]": "Search all commands",
            f"{PREFIX}allhelp": "Overview of all categories",
        }
    },
}


def get_all_categories():
    cats = {}
    for name, data in SCRIPT_CATEGORIES.items():
        cats[name] = data
    for name, data in NATIVE_COMMANDS.items():
        cats[name] = data
    return cats


def get_dynamic_scripts():
    try:
        scripts_path = files.get_scripts_path()
        if not scripts_path or not os.path.isdir(scripts_path):
            return []
        scripts = sorted(f[:-3] for f in os.listdir(scripts_path) if f.endswith(".py"))
        return scripts
    except Exception:
        return []


def _render_category(name, data):
    lines = [f"{data['emoji']} **{name}**\n"]
    for cmd, desc in data["commands"].items():
        lines.append(f"`{cmd}` — {desc}")
    return "\n".join(lines)


@ghost.command(name="shelp", description="Show help for all commands.", usage="[page]")
async def shelp(ctx, page: int = 1):
    categories = list(get_all_categories().items())
    total = len(categories)
    if page < 1 or page > total:
        page = 1

    name, data = categories[page - 1]
    nav = "**Navigate:** " + "  ".join(f"`{i}` {d['emoji']}" for i, (_, d) in enumerate(categories, 1))

    await ctx.send(f"{_render_category(name, data)}\n\n*Page {page}/{total}*\n\n{nav}")


@ghost.command(name="shelprange", description="Show multiple help pages.", usage="[start]-[end]")
async def shelprange(ctx, pages: str = None):
    if not pages:
        await shelp(ctx, 1)
        return

    categories = list(get_all_categories().items())
    total = len(categories)

    try:
        if "-" in pages:
            start, end = (int(x) for x in pages.split("-"))
        else:
            start = end = int(pages)
    except ValueError:
        await ctx.send(f"Usage: `{PREFIX}shelprange 1-3` or `{PREFIX}shelprange 5`")
        return

    start = max(1, start)
    end = min(total, end)
    if start > end:
        start, end = end, start

    result = "\n\n---\n\n".join(_render_category(n, d) for n, d in categories[start - 1:end])
    result += f"\n\n*Showing pages {start}-{end} of {total}*"

    nav = "**Navigate:** " + "  ".join(f"`{i}` {d['emoji']}" for i, (_, d) in enumerate(categories, 1))
    if len(result) > 1900:
        result = result[:1850] + "\n\n*... truncated, use shelp [page] for individual pages*"

    await ctx.send(f"{result}\n\n{nav}")


@ghost.command(name="scmds", description="List all script commands.", usage="")
async def scmds(ctx):
    lines = ["**All Script Commands:**\n"]
    for name, data in SCRIPT_CATEGORIES.items():
        lines.append(f"{data['emoji']} **{name}**")
        for cmd in data["commands"]:
            lines.append(f"  `{cmd}`")
        lines.append("")
    await ctx.send("\n".join(lines))


@ghost.command(name="ncmds", description="List all native Ghost commands.", usage="")
async def ncmds(ctx):
    lines = ["**All Native Ghost Commands:**\n"]
    for name, data in NATIVE_COMMANDS.items():
        lines.append(f"{data['emoji']} **{name}**")
        for cmd in data["commands"]:
            lines.append(f"  `{cmd}`")
        lines.append("")
    await ctx.send("\n".join(lines))


@ghost.command(name="scripts", description="List all loaded scripts.", usage="")
async def scripts_cmd(ctx):
    script_names = get_dynamic_scripts()
    if not script_names:
        await ctx.send("No scripts found in the scripts directory.")
        return
    lines = [f"**Loaded Scripts ({len(script_names)}):**\n"]
    for s in script_names:
        lines.append(f"  `{s}`")
    await ctx.send("\n".join(lines))


@ghost.command(name="cmds", description="Quick command search across all commands.", usage="[query]")
async def cmds(ctx, *, query=None):
    if not query:
        await shelp(ctx, 1)
        return

    query_lower = query.lower()
    results = []

    for cat_name, cat_data in SCRIPT_CATEGORIES.items():
        for cmd, desc in cat_data["commands"].items():
            if query_lower in cmd.lower() or query_lower in desc.lower():
                results.append((cat_data["emoji"], cmd, desc, "Script"))

    for cat_name, cat_data in NATIVE_COMMANDS.items():
        for cmd, desc in cat_data["commands"].items():
            if query_lower in cmd.lower() or query_lower in desc.lower():
                results.append((cat_data["emoji"], cmd, desc, "Native"))

    if not results:
        await ctx.send(f"No commands matching `{query}`.")
        return

    truncated = len(results) > 15
    results = results[:15]

    lines = [f"**Results for `{query}` ({len(results)} shown):**\n"]
    for emoji, cmd, desc, source in results:
        tag = " `[S]`" if source == "Script" else ""
        lines.append(f"{emoji} `{cmd}` — {desc}{tag}")

    if truncated:
        lines.append("\n*... more results. Refine your search.*")

    await ctx.send("\n".join(lines))


@ghost.command(name="allhelp", description="Show overview of all command categories.", usage="")
async def allhelp(ctx):
    categories = list(get_all_categories().items())
    lines = ["**Ghost + Scripts — All Categories**\n"]
    for i, (name, data) in enumerate(categories, 1):
        lines.append(f"{data['emoji']} `{i}` **{name}** ({len(data['commands'])} cmds)")

    script_names = get_dynamic_scripts()
    lines.append(f"\n**Scripts loaded:** {len(script_names)}")
    if script_names:
        lines.append(", ".join(f"`{s}`" for s in script_names))

    lines.append(f"\n*Use `{PREFIX}shelp [page]` or `{PREFIX}shelprange [start]-[end]` for details*")
    lines.append(f"*Use `{PREFIX}cmds [query]` to search all commands*")

    await ctx.send("\n".join(lines))