import random

number_games = {}


@ghost.command(name="numbergame", description="Guess the number the bot is thinking of!", usage="[easy|hard]")
async def numbergame(ctx, difficulty=None):
    if ctx.channel.id in number_games:
        await ctx.send("A number game is already active in this channel!")
        return

    if difficulty and difficulty.lower() == "hard":
        low, high = 1, 1000
    else:
        low, high = 1, 100

    secret = random.randint(low, high)
    number_games[ctx.channel.id] = {"secret": secret, "guesses": 0, "low": low, "high": high}

    await ctx.send(
        f"**Number Game!** I'm thinking of a number between {low} and {high}.\n"
        f"Guess with `.num [number]`"
    )


@ghost.command(name="num", description="Guess a number.", usage="[number]")
async def num(ctx, guess: int = None):
    if ctx.channel.id not in number_games:
        await ctx.send("No active number game. Start one with `.numbergame`")
        return

    if guess is None:
        await ctx.send("Pick a number: `.num 42`")
        return

    game = number_games[ctx.channel.id]
    game["guesses"] += 1

    if guess == game["secret"]:
        await ctx.send(
            f"**Correct!** The number was `{game['secret']}`.\n"
            f"You got it in {game['guesses']} guess{'es' if game['guesses'] != 1 else ''}!"
        )
        del number_games[ctx.channel.id]
    elif guess < game["secret"]:
        await ctx.send(f"Higher! ({game['guesses']} guesses so far)")
    else:
        await ctx.send(f"Lower! ({game['guesses']} guesses so far)")
