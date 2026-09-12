import discord

games = {}


def render_board(board):
    symbols = []
    for cell in board:
        if cell == "X":
            symbols.append("X")
        elif cell == "O":
            symbols.append("O")
        else:
            symbols.append(str(cell))
    return (
        f"```\n"
        f" {symbols[0]} | {symbols[1]} | {symbols[2]}\n"
        f"---+---+---\n"
        f" {symbols[3]} | {symbols[4]} | {symbols[5]}\n"
        f"---+---+---\n"
        f" {symbols[6]} | {symbols[7]} | {symbols[8]}\n"
        f"```"
    )


def check_winner(board, mark):
    wins = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]
    return any(board[i] == board[j] == board[k] == mark for i, j, k in wins)


def is_full(board):
    return all(isinstance(c, str) for c in board)


@ghost.command(name="ttt", description="Play Tic-Tac-Toe against another user.", usage="[@user]")
async def ttt(ctx, opponent: discord.Member = None):
    if opponent is None:
        await ctx.send("Mention a opponent: `.ttt @user`")
        return
    if opponent.id == ctx.author.id:
        await ctx.send("You can't play against yourself!")
        return
    if opponent.bot:
        await ctx.send("You can't play against a bot!")
        return

    games[ctx.channel.id] = {
        "board": list(range(1, 10)),
        "turn": ctx.author.id,
        "players": {ctx.author.id: "X", opponent.id: "O"},
        "names": {ctx.author.id: ctx.author.display_name, opponent.id: opponent.display_name}
    }

    await ctx.send(
        f"**Tic-Tac-Toe!** {ctx.author.display_name} (X) vs {opponent.display_name} (O)\n"
        f"{ctx.author.display_name} goes first!\n"
        f"Use `.ttt [1-9]` to place your mark.\n"
        f"{render_board(games[ctx.channel.id]['board'])}"
    )


@ghost.command(name="ttt", description="Place your mark on the board.", usage="[1-9]")
async def ttt_move(ctx, position: int = None):
    if ctx.channel.id not in games:
        await ctx.send("No active game. Start one with `.ttt @user`")
        return

    game = games[ctx.channel.id]

    if ctx.author.id not in game["players"]:
        await ctx.send("You're not in this game!")
        return

    if game["turn"] != ctx.author.id:
        await ctx.send("It's not your turn!")
        return

    if position is None or position < 1 or position > 9:
        await ctx.send("Pick a position 1-9.")
        return

    idx = position - 1
    if isinstance(game["board"][idx], str):
        await ctx.send("That spot is taken!")
        return

    mark = game["players"][ctx.author.id]
    game["board"][idx] = mark

    if check_winner(game["board"], mark):
        await ctx.send(f"**{game['names'][ctx.author.id]} wins!**\n{render_board(game['board'])}")
        del games[ctx.channel.id]
        return

    if is_full(game["board"]):
        await ctx.send(f"**It's a draw!**\n{render_board(game['board'])}")
        del games[ctx.channel.id]
        return

    other_id = [pid for pid in game["players"] if pid != ctx.author.id][0]
    game["turn"] = other_id

    await ctx.send(
        f"{game['names'][other_id]}'s turn ({game['players'][other_id]})\n"
        f"{render_board(game['board'])}"
    )
