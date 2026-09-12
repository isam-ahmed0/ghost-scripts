import discord

SCRIPT_CATEGORIES = {
    "Utility": {
        "emoji": "🔧",
        "commands": {
            ".autostatus add/remove/list/start/stop": "Rotate custom statuses on a timer",
            ".remind [time] [msg]": "Set a reminder that DMs you after a delay",
            ".reminders": "View your pending reminders",
            ".logchannel #chan": "Start logging a channel to file",
            ".logstop #chan": "Stop logging a channel",
            ".logstatus": "Show logged channels",
            ".mystats": "View your message statistics",
            ".serverstats": "View server-wide message statistics",
            ".pinglog": "Show last 10 pings you received",
            ".pingclear": "Clear ping log",
            ".autonick [names]": "Rotate nicknames on a timer",
            ".autonick stop": "Stop nickname rotation",
            ".dms": "Show last 10 logged DMs",
            ".dmsearch [query]": "Search your DM log",
            ".dmclear": "Clear DM log",
        }
    },
    "Fun": {
        "emoji": "🎉",
        "commands": {
            ".fortune": "Get a random fortune told",
            ".trivia": "Answer a trivia question",
            ".triviascore": "View trivia leaderboard",
            ".compliment @user": "Send 3 random compliments to someone",
        }
    },
    "Games": {
        "emoji": "🎮",
        "commands": {
            ".ttt @user": "Play Tic-Tac-Toe against someone",
            ".ttt [1-9]": "Place your mark on the board",
            ".wordguess": "Start a hangman word game",
            ".guess [letter]": "Guess a letter in word guess",
            ".numbergame [easy/hard]": "Number guessing game (1-100 or 1-1000)",
            ".num [number]": "Guess the number",
            ".adventure": "Start a dungeon adventure",
            ".choice [1-3]": "Make a choice in your adventure",
        }
    },
    "Prank": {
        "emoji": "😈",
        "commands": {
            ".mock [text]": "mOcKiFy TeXt (spongebob case)",
            ".ghostping @user": "Send a ghost ping that auto-deletes",
            ".typingtroll @user": "Show typing for 10-30s then say nothing",
            ".autocorrect [text]": "Autocorrect words to food names",
        }
    },
}


def get_script_help_page(page_num, total):
    categories = list(SCRIPT_CATEGORIES.items())
    cat_name, cat_data = categories[page_num - 1]
    lines = [f"{cat_data['emoji']} **{cat_name}**\n"]
    for cmd, desc in cat_data["commands"].items():
        lines.append(f"`{cmd}` — {desc}")
    lines.append(f"\n*Page {page_num}/{total}*")
    return "\n".join(lines)


@ghost.command(name="shelp", description="Show help for all script commands.", usage="[page]")
async def shelp(ctx, page: int = 1):
    categories = list(SCRIPT_CATEGORIES.items())
    total = len(categories)

    if page < 1 or page > total:
        page = 1

    cat_name, cat_data = categories[page - 1]

    lines = [f"{cat_data['emoji']} **{cat_name}**\n"]
    for cmd, desc in cat_data["commands"].items():
        lines.append(f"`{cmd}` — {desc}")
    lines.append(f"\n*Page {page}/{total}*  |  Use `.shelp [page]` to navigate*")

    nav = "**Pages:** "
    for i, (name, data) in enumerate(categories, 1):
        nav += f"`{i}` {data['emoji']} {name}  "

    await ctx.send(f"{''.join(lines)}\n\n{nav}")


@ghost.command(name="scmds", description="List all script commands.", usage="")
async def scmds(ctx):
    lines = ["**All Script Commands:**\n"]
    for cat_name, cat_data in SCRIPT_CATEGORIES.items():
        lines.append(f"{cat_data['emoji']} **{cat_name}**")
        for cmd in cat_data["commands"]:
            lines.append(f"  `{cmd}`")
        lines.append("")
    await ctx.send("\n".join(lines))


@ghost.command(name="cmds", description="Quick command search.", usage="[query]")
async def cmds(ctx, *, query=None):
    if not query:
        await shelp(ctx)
        return

    query_lower = query.lower()
    results = []
    for cat_name, cat_data in SCRIPT_CATEGORIES.items():
        for cmd, desc in cat_data["commands"].items():
            if query_lower in cmd.lower() or query_lower in desc.lower():
                results.append((cat_data["emoji"], cmd, desc))

    if not results:
        await ctx.send(f"No commands matching `{query}`.")
        return

    lines = [f"**Results for `{query}`:**\n"]
    for emoji, cmd, desc in results:
        lines.append(f"{emoji} `{cmd}` — {desc}")

    await ctx.send("\n".join(lines))
