import random
import asyncio

word_games = {}

word_list = [
    "python", "discord", "programming", "computer", "keyboard",
    "algorithm", "function", "variable", "database", "network",
    "server", "internet", "browser", "website", "software",
    "hardware", "terminal", "command", "debug", "compile",
    "syntax", "module", "package", "library", "framework",
    "algorithm", "encrypt", "decrypt", "binary", "pixel",
    "dragon", "wizard", "castle", "dungeon", "potion",
    "shield", "sword", "quest", "treasure", "monster",
    "galaxy", "planet", "rocket", "nebula", "asteroid",
    "whisper", "shadow", "phoenix", "crystal", "thunder",
]


@ghost.command(name="wordguess", description="Play a hangman word guessing game!", usage="")
async def wordguess(ctx):
    if ctx.channel.id in word_games:
        await ctx.send("A word game is already active in this channel!")
        return

    word = random.choice(word_list)
    revealed = ["_"] * len(word)
    wrong_guesses = []
    max_wrong = 6

    word_games[ctx.channel.id] = {
        "word": word,
        "revealed": revealed,
        "wrong": wrong_guesses,
    }

    await ctx.send(
        f"**Word Guessing Game!**\n"
        f"The word has {len(word)} letters.\n"
        f"```\nWord: {' '.join(revealed)}\nWrong: {', '.join(wrong_guesses) or 'none'}\nLives: {max_wrong - len(wrong_guesses)}\n```\n"
        f"Guess a letter with `.guess [letter]`"
    )


@ghost.command(name="guess", description="Guess a letter in word guess.", usage="[letter]")
async def guess(ctx, letter=None):
    if ctx.channel.id not in word_games:
        await ctx.send("No active word game. Start one with `.wordguess`")
        return

    if not letter or len(letter) != 1 or not letter.isalpha():
        await ctx.send("Guess a single letter: `.guess a`")
        return

    game = word_games[ctx.channel.id]
    letter = letter.lower()

    if letter in game["revealed"] or letter in game["wrong"]:
        await ctx.send(f"You already guessed `{letter}`!")
        return

    if letter in game["word"]:
        for i, ch in enumerate(game["word"]):
            if ch == letter:
                game["revealed"][i] = letter
    else:
        game["wrong"].append(letter)

    wrong_count = len(game["wrong"])

    if wrong_count >= 6:
        await ctx.send(
            f"**Game Over!** The word was `{game['word']}`.\n"
            f"```\nWord: {' '.join(game['revealed'])}\nWrong: {', '.join(game['wrong'])}\n```"
        )
        del word_games[ctx.channel.id]
        return

    if "_" not in game["revealed"]:
        await ctx.send(
            f"**You won!** The word was `{game['word']}`!\n"
            f"Guessed in {wrong_count} wrong guesses."
        )
        del word_games[ctx.channel.id]
        return

    display = []
    for i, ch in enumerate(game["word"]):
        if game["revealed"][i] != "_":
            display.append(game["revealed"][i])
        else:
            display.append("_")

    await ctx.send(
        f"```\nWord: {' '.join(display)}\nWrong: {', '.join(game['wrong']) or 'none'}\n"
        f"Lives: {6 - wrong_count}\n```"
    )
