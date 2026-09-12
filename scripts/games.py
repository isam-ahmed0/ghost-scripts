import random
import asyncio

PREFIX = ghost.command_prefix


# ─────────────────────────────────────────────
#  Adventure game
# ─────────────────────────────────────────────

adventure_games = {}


def get_scenes():
    return {
        "start": {
            "text": "You wake up in a dark dungeon. Torches flicker on the walls.\nYou see two passages ahead.",
            "choices": {
                "1": {"text": "Take the left passage", "next": "left_passage"},
                "2": {"text": "Take the right passage", "next": "right_passage"},
                "3": {"text": "Search the room", "next": "search_room"},
            }
        },
        "search_room": {
            "text": "You find a rusty key and a health potion hidden under a loose stone!",
            "gold": 10,
            "items": ["rusty key", "health potion"],
            "choices": {
                "1": {"text": "Take the left passage", "next": "left_passage"},
                "2": {"text": "Take the right passage", "next": "right_passage"},
            }
        },
        "left_passage": {
            "text": "The passage leads to a goblin camp. A goblin guard spots you!",
            "choices": {
                "1": {"text": "Fight the goblin", "next": "fight_goblin", "hp_cost": 20},
                "2": {"text": "Sneak past", "next": "sneak_past"},
                "3": {"text": "Run back", "next": "start"},
            }
        },
        "fight_goblin": {
            "text": "You defeat the goblin and find 15 gold coins!",
            "gold": 15,
            "choices": {
                "1": {"text": "Continue deeper", "next": "treasure_room"},
                "2": {"text": "Go back", "next": "start"},
            }
        },
        "sneak_past": {
            "text": "You tiptoe past the goblin... but he spots you!",
            "choices": {
                "1": {"text": "Fight!", "next": "fight_goblin", "hp_cost": 10},
                "2": {"text": "Run back", "next": "start"},
            }
        },
        "right_passage": {
            "text": "You find a sparkling treasure chest guarded by a skeleton!",
            "choices": {
                "1": {"text": "Fight the skeleton", "next": "fight_skeleton", "hp_cost": 25},
                "2": {"text": "Try to open the chest anyway", "next": "open_chest"},
                "3": {"text": "Go back", "next": "start"},
            }
        },
        "fight_skeleton": {
            "text": "You shatter the skeleton and claim the treasure! 30 gold!",
            "gold": 30,
            "choices": {
                "1": {"text": "Explore more", "next": "treasure_room"},
                "2": {"text": "Go back", "next": "start"},
            }
        },
        "open_chest": {
            "text": "The skeleton attacks you as you reach for the chest!",
            "hp_cost": 15,
            "choices": {
                "1": {"text": "Fight back!", "next": "fight_skeleton"},
                "2": {"text": "Flee!", "next": "start"},
            }
        },
        "treasure_room": {
            "text": "A massive door stands before you. You see a dragon sleeping on a pile of gold!",
            "choices": {
                "1": {"text": "Fight the dragon", "next": "fight_dragon", "hp_cost": 40},
                "2": {"text": "Steal some gold quietly", "next": "steal_gold"},
                "3": {"text": "Leave quietly", "next": "ending_escape"},
            }
        },
        "steal_gold": {
            "text": "You grab as much gold as you can! 50 gold! But the dragon stirs...",
            "gold": 50,
            "choices": {
                "1": {"text": "Fight the dragon!", "next": "fight_dragon", "hp_cost": 40},
                "2": {"text": "Run for your life!", "next": "ending_escape"},
            }
        },
        "fight_dragon": {
            "text": "An epic battle! You slay the dragon and claim ALL its treasure! 100 gold!",
            "gold": 100,
            "next": "ending_victory",
        },
        "ending_victory": {
            "text": "You emerge from the dungeon wealthy and victorious! A true hero!",
            "choices": {},
            "end": True,
        },
        "ending_escape": {
            "text": "You escape the dungeon alive. Safe, but not rich. Better luck next time!",
            "choices": {},
            "end": True,
        },
    }


@ghost.command(name="adventure", description="Start a dungeon adventure!", usage="")
async def adventure(ctx):
    if ctx.channel.id in adventure_games:
        await ctx.send(f"An adventure is already active! Use `{PREFIX}choice [1-3]`")
        return

    adventure_games[ctx.channel.id] = {"hp": 100, "gold": 0, "items": [], "scene": "start"}
    await _send_scene(ctx, get_scenes()["start"], adventure_games[ctx.channel.id])


async def _send_scene(ctx, scene, game):
    choices_text = "\n".join(f"  {k}. {v['text']}" for k, v in scene["choices"].items())
    items_str = f"\nItems: {', '.join(game['items'])}" if game["items"] else ""
    await ctx.send(
        f"**Dungeon Adventure!**\n\n{scene['text']}\n\n"
        f"```\n{choices_text}\n```\n"
        f"HP: {game['hp']} | Gold: {game['gold']}{items_str}\n"
        f"Choose with `{PREFIX}choice [number]`"
    )


@ghost.command(name="choice", description="Make a choice in your adventure.", usage="[1-3]")
async def choice(ctx, num=None):
    if ctx.channel.id not in adventure_games:
        await ctx.send(f"No active adventure. Start one with `{PREFIX}adventure`")
        return

    if num is None or num not in ("1", "2", "3"):
        await ctx.send(f"Pick a choice: `{PREFIX}choice 1`")
        return

    game = adventure_games[ctx.channel.id]
    scenes = get_scenes()
    scene = scenes[game["scene"]]

    if num not in scene.get("choices", {}):
        await ctx.send("Invalid choice!")
        return

    chosen = scene["choices"][num]
    hp_cost = chosen.get("hp_cost", 0)
    game["hp"] -= hp_cost

    if game["hp"] <= 0:
        await ctx.send("**You have been defeated!** Game over.")
        del adventure_games[ctx.channel.id]
        return

    next_scene = scenes[chosen["next"]]
    game["gold"] += next_scene.get("gold", 0)
    game["items"].extend(next_scene.get("items", []))
    game["scene"] = chosen["next"]

    if hp_cost > 0:
        await ctx.send(f"**-{hp_cost} HP** from the battle!")

    if next_scene.get("end") or not next_scene.get("choices", {}):
        items_str = f"\nItems: {', '.join(game['items'])}" if game["items"] else ""
        await ctx.send(
            f"**Adventure Complete!**\n\n{next_scene['text']}\n\n"
            f"Final HP: {game['hp']} | Gold: {game['gold']}{items_str}"
        )
        del adventure_games[ctx.channel.id]
        return

    await _send_scene(ctx, next_scene, game)


# ─────────────────────────────────────────────
#  Number guessing game
# ─────────────────────────────────────────────

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

    number_games[ctx.channel.id] = {"secret": random.randint(low, high), "guesses": 0}
    await ctx.send(
        f"**Number Game!** I'm thinking of a number between {low} and {high}.\n"
        f"Guess with `{PREFIX}num [number]`"
    )


@ghost.command(name="num", description="Guess a number.", usage="[number]")
async def num(ctx, guess: int = None):
    if ctx.channel.id not in number_games:
        await ctx.send(f"No active number game. Start one with `{PREFIX}numbergame`")
        return

    if guess is None:
        await ctx.send(f"Pick a number: `{PREFIX}num 42`")
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


# ─────────────────────────────────────────────
#  Word guessing game
# ─────────────────────────────────────────────

word_games = {}

word_list = [
    "python", "discord", "programming", "computer", "keyboard",
    "algorithm", "function", "variable", "database", "network",
    "server", "internet", "browser", "website", "software",
    "hardware", "terminal", "command", "debug", "compile",
    "syntax", "module", "package", "library", "framework",
    "encrypt", "decrypt", "binary", "pixel",
    "dragon", "wizard", "castle", "dungeon", "potion",
    "shield", "sword", "quest", "treasure", "monster",
    "galaxy", "planet", "rocket", "nebula", "asteroid",
    "whisper", "shadow", "phoenix", "crystal", "thunder",
]


def render_word_game(game):
    return (
        f"```\nWord: {' '.join(game['revealed'])}\n"
        f"Wrong: {', '.join(game['wrong']) or 'none'}\n"
        f"Lives: {6 - len(game['wrong'])}\n```"
    )


@ghost.command(name="wordguess", description="Play a hangman word guessing game!", usage="")
async def wordguess(ctx):
    if ctx.channel.id in word_games:
        await ctx.send("A word game is already active in this channel!")
        return

    word = random.choice(word_list)
    word_games[ctx.channel.id] = {"word": word, "revealed": ["_"] * len(word), "wrong": []}

    await ctx.send(
        f"**Word Guessing Game!**\nThe word has {len(word)} letters.\n"
        f"{render_word_game(word_games[ctx.channel.id])}\n"
        f"Guess a letter with `{PREFIX}guess [letter]`"
    )


@ghost.command(name="guess", description="Guess a letter in word guess.", usage="[letter]")
async def guess(ctx, letter=None):
    if ctx.channel.id not in word_games:
        await ctx.send(f"No active word game. Start one with `{PREFIX}wordguess`")
        return

    if not letter or len(letter) != 1 or not letter.isalpha():
        await ctx.send(f"Guess a single letter: `{PREFIX}guess a`")
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
        await ctx.send(f"**Game Over!** The word was `{game['word']}`.\n{render_word_game(game)}")
        del word_games[ctx.channel.id]
        return

    if "_" not in game["revealed"]:
        await ctx.send(f"**You won!** The word was `{game['word']}`!\nGuessed in {wrong_count} wrong guesses.")
        del word_games[ctx.channel.id]
        return

    await ctx.send(render_word_game(game))


# ─────────────────────────────────────────────
#  Tic-Tac-Toe (start with @user, move with 1-9)
# ─────────────────────────────────────────────

ttt_games = {}


def render_ttt_board(board):
    symbols = [str(c) if not isinstance(c, str) else c for c in board]
    return (
        f"```\n {symbols[0]} | {symbols[1]} | {symbols[2]}\n"
        f"---+---+---\n {symbols[3]} | {symbols[4]} | {symbols[5]}\n"
        f"---+---+---\n {symbols[6]} | {symbols[7]} | {symbols[8]}\n```"
    )


def ttt_winner(board, mark):
    wins = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]
    return any(board[i] == board[j] == board[k] == mark for i, j, k in wins)


def ttt_full(board):
    return all(isinstance(c, str) for c in board)


@ghost.command(name="ttt", description="Play Tic-Tac-Toe. Mention a user to start, or pass 1-9 to move.", usage="[@user] | [1-9]")
async def ttt(ctx, *args):
    game = ttt_games.get(ctx.channel.id)

    if not args:
        if game:
            await ctx.send(f"Active game! Move with `{PREFIX}ttt [1-9]`")
        else:
            await ctx.send(f"Start a game: `{PREFIX}ttt @user`")
        return

    if str(args[0]).isdigit():
        await ttt_move(ctx, int(args[0]))
        return

    mentions = ctx.message.mentions
    if not mentions:
        await ctx.send(f"Mention an opponent to start: `{PREFIX}ttt @user`")
        return

    opponent = mentions[0]
    if opponent.id == ctx.author.id:
        await ctx.send("You can't play against yourself!")
        return
    if opponent.bot:
        await ctx.send("You can't play against a bot!")
        return

    ttt_games[ctx.channel.id] = {
        "board": list(range(1, 10)),
        "turn": ctx.author.id,
        "players": {ctx.author.id: "X", opponent.id: "O"},
        "names": {ctx.author.id: ctx.author.display_name, opponent.id: opponent.display_name}
    }

    await ctx.send(
        f"**Tic-Tac-Toe!** {ctx.author.display_name} (X) vs {opponent.display_name} (O)\n"
        f"{ctx.author.display_name} goes first!\n"
        f"Use `{PREFIX}ttt [1-9]` to place your mark.\n"
        f"{render_ttt_board(ttt_games[ctx.channel.id]['board'])}"
    )


async def ttt_move(ctx, position):
    game = ttt_games.get(ctx.channel.id)
    if not game:
        await ctx.send(f"No active game. Start one with `{PREFIX}ttt @user`")
        return

    if ctx.author.id not in game["players"]:
        await ctx.send("You're not in this game!")
        return

    if game["turn"] != ctx.author.id:
        await ctx.send("It's not your turn!")
        return

    if position < 1 or position > 9:
        await ctx.send("Pick a position 1-9.")
        return

    idx = position - 1
    if isinstance(game["board"][idx], str):
        await ctx.send("That spot is taken!")
        return

    mark = game["players"][ctx.author.id]
    game["board"][idx] = mark
    board = game["board"]

    if ttt_winner(board, mark):
        await ctx.send(f"**{game['names'][ctx.author.id]} wins!**\n{render_ttt_board(board)}")
        del ttt_games[ctx.channel.id]
        return

    if ttt_full(board):
        await ctx.send(f"**It's a draw!**\n{render_ttt_board(board)}")
        del ttt_games[ctx.channel.id]
        return

    other_id = next(pid for pid in game["players"] if pid != ctx.author.id)
    game["turn"] = other_id

    await ctx.send(
        f"{game['names'][other_id]}'s turn ({game['players'][other_id]})\n"
        f"{render_ttt_board(board)}"
    )


# ─────────────────────────────────────────────
#  Trivia
# ─────────────────────────────────────────────

trivia_scores = {}
active_trivia = []

questions = [
    {"q": "What planet is known as the Red Planet?", "options": ["Venus", "Mars", "Jupiter", "Saturn"], "answer": 2},
    {"q": "What is the largest ocean on Earth?", "options": ["Atlantic", "Indian", "Arctic", "Pacific"], "answer": 4},
    {"q": "How many continents are there?", "options": ["5", "6", "7", "8"], "answer": 3},
    {"q": "What gas do plants absorb from the atmosphere?", "options": ["Oxygen", "Nitrogen", "Carbon Dioxide", "Hydrogen"], "answer": 3},
    {"q": "What is the hardest natural substance?", "options": ["Gold", "Iron", "Diamond", "Quartz"], "answer": 3},
    {"q": "How many bones are in the adult human body?", "options": ["106", "206", "306", "186"], "answer": 2},
    {"q": "What is the speed of light in km/s (approximately)?", "options": ["150,000", "300,000", "450,000", "600,000"], "answer": 2},
    {"q": "Which country has the most people?", "options": ["USA", "India", "China", "Russia"], "answer": 3},
    {"q": "What is the largest mammal?", "options": ["Elephant", "Blue Whale", "Giraffe", "Hippopotamus"], "answer": 2},
    {"q": "In what year did World War II end?", "options": ["1943", "1944", "1945", "1946"], "answer": 3},
    {"q": "What is the chemical symbol for water?", "options": ["H2O", "CO2", "NaCl", "O2"], "answer": 1},
    {"q": "How many sides does a hexagon have?", "options": ["5", "6", "7", "8"], "answer": 2},
    {"q": "What is the smallest prime number?", "options": ["0", "1", "2", "3"], "answer": 3},
    {"q": "Which planet has the most moons?", "options": ["Jupiter", "Saturn", "Uranus", "Neptune"], "answer": 2},
    {"q": "What element does 'O' represent?", "options": ["Gold", "Osmium", "Oxygen", "Oganesson"], "answer": 3},
    {"q": "What is the capital of Japan?", "options": ["Seoul", "Beijing", "Tokyo", "Bangkok"], "answer": 3},
    {"q": "How many colors are in a rainbow?", "options": ["5", "6", "7", "8"], "answer": 3},
    {"q": "What is the largest desert?", "options": ["Sahara", "Arabian", "Antarctic", "Gobi"], "answer": 3},
    {"q": "Who painted the Mona Lisa?", "options": ["Van Gogh", "Picasso", "Da Vinci", "Monet"], "answer": 3},
    {"q": "What is the boiling point of water in Celsius?", "options": ["90", "100", "110", "120"], "answer": 2},
]


@ghost.command(name="trivia", description="Play a trivia game!", usage="")
async def trivia(ctx):
    if ctx.channel.id in active_trivia:
        await ctx.send("A trivia question is already active in this channel!")
        return

    q = random.choice(questions)
    active_trivia.append(ctx.channel.id)

    options_text = "\n".join(f"  {i}. {opt}" for i, opt in enumerate(q["options"], 1))
    await ctx.send(
        f"**Trivia Time!**\n\n{q['q']}\n\n"
        f"```\n{options_text}\n```\n"
        f"Type the number (1-4) to answer. You have 30 seconds!"
    )

    def check(m):
        return m.channel.id == ctx.channel.id and m.author.id == ctx.author.id and m.content.strip().isdigit()

    try:
        guess = await ghost.wait_for("message", check=check, timeout=30)
        answer = int(guess.content.strip())
        if answer == q["answer"]:
            uid = ctx.author.id
            trivia_scores[uid] = trivia_scores.get(uid, 0) + 1
            await ctx.send(
                f"**Correct!** `{q['options'][q['answer'] - 1]}` is the right answer.\n"
                f"Score: {trivia_scores[uid]}"
            )
        else:
            await ctx.send(f"**Wrong!** The answer was `{q['options'][q['answer'] - 1]}`.")
    except asyncio.TimeoutError:
        await ctx.send(f"**Time's up!** The answer was `{q['options'][q['answer'] - 1]}`.")
    finally:
        if ctx.channel.id in active_trivia:
            active_trivia.remove(ctx.channel.id)


@ghost.command(name="triviascore", description="View trivia leaderboard.", usage="")
async def triviascore(ctx):
    if not trivia_scores:
        await ctx.send("No trivia scores yet.")
        return

    top = sorted(trivia_scores.items(), key=lambda x: x[1], reverse=True)[:10]
    lines = []
    for i, (uid, score) in enumerate(top, 1):
        member = ctx.guild.get_member(uid) if ctx.guild else None
        name = member.display_name if member else str(uid)
        lines.append(f"  {i}. {name}: {score}")
    await ctx.send(f"```\nTrivia Leaderboard:\n{chr(10).join(lines)}\n```")