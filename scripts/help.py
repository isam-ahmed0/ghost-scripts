import os
import importlib

NATIVE_COMMANDS = {
    "General": {
        "emoji": "📖",
        "commands": {
            ".help": "A list of all categories",
            ".ping": "Check the bot's latency",
            ".search [query] [page]": "Search for commands",
        }
    },
    "Account": {
        "emoji": "👤",
        "commands": {
            ".account": "Account commands",
            ".backups": "List your backups",
            ".backup create/delete/restore/view": "Backup management",
            ".hypesquad [house]": "Change your hypesquad",
            ".status [status]": "Change your online status",
            ".customstatus [status]": "Change your custom status",
            ".clearstatus": "Clear your custom status",
            ".playing [status]": "Set a playing status",
            ".streaming [status]": "Set a streaming status",
            ".nickname [name]": "Change your server nickname",
            ".clearnickname": "Clear your nickname",
            ".discordtheme [theme]": "Change Discord theme",
            ".yoinkrpc [user]": "Steal someone's rich presence",
        }
    },
    "Fun": {
        "emoji": "🎉",
        "commands": {
            ".rickroll": "Never gonna give you up",
            ".coinflip": "Flip a coin",
            ".iq [user]": "Get the IQ of a user",
            ".howgay [user]": "Get the gayness of a user",
            ".howblack [user]": "Get the blackness of a user",
            ".pp [user]": "Get the pp size",
            ".rps": "Play rock paper scissors",
            ".slots": "Play a slot machine",
            ".encodemorsecode [text]": "Encode text to morse code",
            ".decodemorsecode [morse]": "Decode morse code",
            ".blocksend [user] [msg]": "Send message to blocked user",
            ".randomdata [type]": "Generate random data",
            ".kanye": "Random Kanye quote",
            ".socialcredit [user]": "Social credit score",
            ".dice [sides]": "Roll a dice",
            ".rainbow [text]": "Create rainbow text",
            ".rainbowreact [msg id]": "Rainbow reaction",
            ".dox [user]": "Dox a user (fake)",
            ".meme": "Get a random meme",
            ".dadjoke": "Get a dad joke",
            ".insult": "Get a random insult",
            ".compliment [user]": "Get a random compliment",
            ".catfact": "Get a random cat fact",
            ".yomomma": "Get a yo momma joke",
            ".8ball [question]": "Ask the magic 8ball",
            ".fakenitro": "Fake a nitro gift",
            ".hyperlink [link] [text]": "Create a hyperlink",
            ".aura [user]": "Check a user's aura",
            ".gyatt [user]": "Check if they've got GYATTT",
            ".playsound [url]": "Play a 5 second sound",
        }
    },
    "Image": {
        "emoji": "🖼️",
        "commands": {
            ".gato": "Get a random cat picture",
            ".doggo": "Get a random dog picture",
            ".bird": "Get a random bird picture",
            ".fox": "Get a random fox picture",
            ".minion": "Get a random minion meme",
            ".achievement [icon] [text]": "Minecraft achievement",
            ".challenge [icon] [text]": "Minecraft challenge",
            ".discordmessage [user] [msg]": "Fake Discord message",
            ".searchimage [query]": "Google image search",
        }
    },
    "Info": {
        "emoji": "ℹ️",
        "commands": {
            ".iplookup [ip]": "Look up an IP address",
            ".userinfo [user]": "Get user information",
            ".serverinfo": "Get server information",
            ".servericon": "Get the server icon",
            ".webhookinfo [url]": "Get webhook information",
            ".mutualservers [user]": "List mutual servers",
            ".avatar [user]": "Get a user's avatar",
            ".tickets": "List all tickets",
            ".hiddenchannels": "List all hidden channels",
            ".crypto [coin]": "Cryptocurrency data",
            ".bitcoin / .ethereum / .tether / .dogecoin": "Quick crypto prices",
            ".timestamp": "Create Discord timestamps",
        }
    },
    "Mod": {
        "emoji": "🛡️",
        "commands": {
            ".clear [amount]": "Clear messages",
            ".dmpurge [user]": "Purge DMs",
            ".purgechat": "Purge chat",
            ".dumpchat": "Export chat history",
            ".firstmessage": "Get first message in channel",
            ".lock [channel]": "Lock a channel",
            ".unlock [channel]": "Unlock a channel",
            ".banlist": "List bans",
            ".ban [user]": "Ban a user",
            ".unban [user]": "Unban a user",
            ".kick [user]": "Kick a user",
            ".mute [user]": "Mute a user",
            ".unmute [user]": "Unmute a user",
            ".poll [question]": "Create a poll",
            ".discordpoll": "Create a Discord poll",
        }
    },
    "Text": {
        "emoji": "✏️",
        "commands": {
            ".shrug": "Shrug your arms",
            ".tableflip": "Flip the table",
            ".unflip": "Put the table back",
            ".lmgtfy [search]": "Let me Google that for you",
            ".blank": "Send a blank message",
            ".fakepurge": "Flood chat with blank messages",
            ".ascii [text]": "Create ASCII text art",
            ".aesthetic [text]": "Make text aesthetic",
            ".chatbypass [text]": "Bypass chat filters",
            ".regional [text]": "Text out of emojis",
            ".randomcase [text]": "Random case text",
            ".animate [text]": "Animate text",
            ".cembed [title] [desc] [footer] [colour]": "Custom embed builder",
            ".passwordgen [length]": "Generate a password",
            ".codeblock [lang] [code]": "Create a codeblock",
            ".json / .python / .js / .html / .css": "Language codeblocks",
            ".java / .c / .cpp / .php / .lua": "More codeblocks",
            ".reverse [text]": "Reverse your text",
        }
    },
    "Theming": {
        "emoji": "🎨",
        "commands": {
            ".themes [page]": "List all themes",
            ".theme create/delete/set": "Theme management",
            ".theme title/colour/footer/image/style": "Edit theme properties",
            ".imagemode": "Set theme to image style",
            ".textmode": "Set theme to codeblock style",
            ".embedmode": "Set theme to embed style",
        }
    },
    "Util": {
        "emoji": "🧰",
        "commands": {
            ".config": "View config (redacted)",
            ".config set [key] [value]": "Set a config value",
            ".restart": "Restart the bot",
            ".quit": "Quit the bot",
            ".settings": "View bot settings",
            ".prefix [prefix]": "Change command prefix",
            ".clearcache": "Clear the cache",
            ".richpresence": "Toggle rich presence",
            ".resetrichpresence": "Reset RPC to defaults",
            ".specs": "View computer specs",
            ".sessionspoofer [device]": "Spoof session device",
            ".uptime": "View bot uptime",
            ".latency": "Check bot latency",
            ".allcmds": "Export all commands to file",
            ".clearconsole": "Clear the console",
            ".commandhistory": "Command usage history",
            ".telemetry": "Toggle telemetry",
            ".telemetryinfo": "View telemetry info",
        }
    },
    "Sniper": {
        "emoji": "🎯",
        "commands": {
            ".snipers": "List all snipers",
            ".sniperstatus [sniper]": "Check sniper status",
            ".nitrosniper [on/off]": "Toggle Nitro sniper",
            ".privnotesniper [on/off]": "Toggle Privnote sniper",
            ".ignoreinvalidcodes [sniper]": "Toggle invalid code handling",
            ".webhooksetup": "Setup snipe webhooks",
        }
    },
    "Abuse": {
        "emoji": "⚠️",
        "commands": {
            ".spam [amount] [msg]": "Spam a channel",
            ".servernuke": "Nuke a server",
            ".channelflood [name]": "Flood guild with channels",
            ".channelspam [amount] [msg]": "Flood a channel",
            ".channelping [user] [amount]": "Ping user in all channels",
            ".massping": "Ping every user in server",
            ".pollspam": "Flood with polls",
        }
    },
    "NSFW": {
        "emoji": "🔞",
        "commands": {
            ".hentai": "Random hentai",
            ".thighs": "Random thigh pic",
            ".ass": "Random ass pic",
            ".boobs": "Random boobs pic",
            ".pussy": "Random pussy pic",
            ".porn": "Random porn",
            ".neko": "Random neko pic",
        }
    },
}

SCRIPT_CATEGORIES = {
    "Script Utility": {
        "emoji": "🔧",
        "commands": {
            ".autostatus add/remove/list/start/stop": "Rotate custom statuses on a timer",
            ".statuslist": "Quick alias for status list",
            ".remind [time] [msg]": "Set a reminder that DMs you after a delay",
            ".reminders": "View your pending reminders",
            ".logchannel #chan": "Start logging a channel to file",
            ".logstop #chan": "Stop logging a channel",
            ".logstatus": "Show logged channels",
            ".mystats": "View your message statistics",
            ".serverstats": "View server-wide statistics",
            ".pinglog": "Show last 10 pings you received",
            ".pingclear": "Clear ping log",
            ".autonick [names]": "Rotate nicknames on a timer",
            ".autonick stop": "Stop nickname rotation",
            ".dms": "Show last 10 logged DMs",
            ".dmsearch [query]": "Search your DM log",
            ".dmclear": "Clear DM log",
        }
    },
    "Script Fun": {
        "emoji": "🎲",
        "commands": {
            ".fortune": "Get a random fortune told",
            ".trivia": "Play a trivia question",
            ".triviascore": "View trivia leaderboard",
            ".complimentbomb @user": "Send 3 compliments to someone",
        }
    },
    "Script Games": {
        "emoji": "🎮",
        "commands": {
            ".ttt @user": "Play Tic-Tac-Toe",
            ".ttt [1-9]": "Place your mark on the board",
            ".wordguess": "Start a hangman word game",
            ".guess [letter]": "Guess a letter",
            ".numbergame [easy/hard]": "Number guessing game",
            ".num [number]": "Guess the number",
            ".adventure": "Start a dungeon adventure",
            ".choice [1-3]": "Make a choice in adventure",
        }
    },
    "Script Prank": {
        "emoji": "😈",
        "commands": {
            ".mock [text]": "mOcKiFy TeXt (spongebob case)",
            ".ghostping @user": "Ghost ping that auto-deletes",
            ".typingtroll @user": "Type for 10-30s then say nothing",
            ".autocorrect [text]": "Correct words to food names",
        }
    },
}


def get_all_categories():
    all_cats = {}
    for name, data in SCRIPT_CATEGORIES.items():
        all_cats[name] = data
    for name, data in NATIVE_COMMANDS.items():
        all_cats[name] = data
    return all_cats


def get_dynamic_scripts():
    try:
        scripts_path = files.get_scripts_path()
        if not scripts_path or not os.path.isdir(scripts_path):
            return []
        scripts = [f[:-3] for f in os.listdir(scripts_path) if f.endswith(".py")]
        scripts.sort()
        return scripts
    except Exception:
        return []


@ghost.command(name="shelp", description="Show help for all commands. Usage: .shelp [page]", usage="[page]")
async def shelp(ctx, page: int = 1):
    all_cats = get_all_categories()
    categories = list(all_cats.items())
    total = len(categories)

    if page < 1 or page > total:
        page = 1

    cat_name, cat_data = categories[page - 1]

    lines = [f"{cat_data['emoji']} **{cat_name}**\n"]
    for cmd, desc in cat_data["commands"].items():
        lines.append(f"`{cmd}` — {desc}")

    lines.append(f"\n*Page {page}/{total}*")

    nav = "**Navigate:** "
    for i, (name, data) in enumerate(categories, 1):
        nav += f"`{i}` {data['emoji']}  "

    await ctx.send(f"{''.join(lines)}\n\n{nav}")


@ghost.command(name="shelprange", description="Show multiple help pages. Usage: .shelprange [start]-[end]", usage="[start]-[end]")
async def shelprange(ctx, pages: str = None):
    if not pages:
        await shelp(ctx, 1)
        return

    all_cats = get_all_categories()
    categories = list(all_cats.items())
    total = len(categories)

    try:
        if "-" in pages:
            parts = pages.split("-")
            start = int(parts[0])
            end = int(parts[1])
        else:
            start = int(pages)
            end = start
    except ValueError:
        await ctx.send("Usage: `.shelprange 1-3` or `.shelprange 5`")
        return

    start = max(1, start)
    end = min(total, end)

    if start > end:
        start, end = end, start

    all_lines = []
    for i in range(start - 1, end):
        cat_name, cat_data = categories[i]
        page_lines = [f"{cat_data['emoji']} **{cat_name}**\n"]
        for cmd, desc in cat_data["commands"].items():
            page_lines.append(f"`{cmd}` — {desc}")
        page_lines.append("")
        all_lines.append("\n".join(page_lines))

    result = "\n---\n".join(all_lines)
    result += f"\n*Showing pages {start}-{end} of {total}*"

    nav = "**Navigate:** "
    for i, (name, data) in enumerate(categories, 1):
        nav += f"`{i}` {data['emoji']}  "

    if len(result) > 1900:
        result = result[:1850] + "\n\n*... truncated, use .shelp [page] for individual pages*"

    await ctx.send(f"{result}\n\n{nav}")


@ghost.command(name="scmds", description="List all script commands.", usage="")
async def scmds(ctx):
    lines = ["**All Script Commands:**\n"]
    for cat_name, cat_data in SCRIPT_CATEGORIES.items():
        lines.append(f"{cat_data['emoji']} **{cat_name}**")
        for cmd in cat_data["commands"]:
            lines.append(f"  `{cmd}`")
        lines.append("")
    await ctx.send("\n".join(lines))


@ghost.command(name="ncmds", description="List all native Ghost commands.", usage="")
async def ncmds(ctx):
    lines = ["**All Native Ghost Commands:**\n"]
    for cat_name, cat_data in NATIVE_COMMANDS.items():
        lines.append(f"{cat_data['emoji']} **{cat_name}**")
        for cmd in cat_data["commands"]:
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

    if len(results) > 15:
        results = results[:15]
        truncated = True
    else:
        truncated = False

    lines = [f"**Results for `{query}` ({len(results)} shown):**\n"]
    for emoji, cmd, desc, source in lines_label := results:
        tag = " `[S]`" if source == "Script" else ""
        lines.append(f"{emoji} `{cmd}` — {desc}{tag}")

    if truncated:
        lines.append(f"\n*... more results. Refine your search.*")

    await ctx.send("\n".join(lines))


@ghost.command(name="allhelp", description="Show overview of all command categories.", usage="")
async def allhelp(ctx):
    all_cats = get_all_categories()
    categories = list(all_cats.items())
    total = len(categories)

    lines = ["**Ghost + Scripts — All Categories**\n"]
    for i, (cat_name, cat_data) in enumerate(categories, 1):
        count = len(cat_data["commands"])
        lines.append(f"{cat_data['emoji']} `{i}` **{cat_name}** ({count} cmds)")

    script_names = get_dynamic_scripts()
    lines.append(f"\n**Scripts loaded:** {len(script_names)}")
    if script_names:
        lines.append(", ".join(f"`{s}`" for s in script_names))

    lines.append(f"\n*Use `.shelp [page]` or `.shelprange [start]-[end]` for details*")
    lines.append(f"*Use `.cmds [query]` to search all commands*")

    await ctx.send("\n".join(lines))
