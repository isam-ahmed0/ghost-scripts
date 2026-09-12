import random
import asyncio

trivia_scores = {}
active_trivia = set()

questions = [
    {
        "q": "What planet is known as the Red Planet?",
        "options": ["Venus", "Mars", "Jupiter", "Saturn"],
        "answer": 2
    },
    {
        "q": "What is the largest ocean on Earth?",
        "options": ["Atlantic", "Indian", "Arctic", "Pacific"],
        "answer": 4
    },
    {
        "q": "How many continents are there?",
        "options": ["5", "6", "7", "8"],
        "answer": 3
    },
    {
        "q": "What gas do plants absorb from the atmosphere?",
        "options": ["Oxygen", "Nitrogen", "Carbon Dioxide", "Hydrogen"],
        "answer": 3
    },
    {
        "q": "What is the hardest natural substance?",
        "options": ["Gold", "Iron", "Diamond", "Quartz"],
        "answer": 3
    },
    {
        "q": "How many bones are in the adult human body?",
        "options": ["106", "206", "306", "186"],
        "answer": 2
    },
    {
        "q": "What is the speed of light in km/s (approximately)?",
        "options": ["150,000", "300,000", "450,000", "600,000"],
        "answer": 2
    },
    {
        "q": "Which country has the most people?",
        "options": ["USA", "India", "China", "Russia"],
        "answer": 3
    },
    {
        "q": "What is the largest mammal?",
        "options": ["Elephant", "Blue Whale", "Giraffe", "Hippopotamus"],
        "answer": 2
    },
    {
        "q": "In what year did World War II end?",
        "options": ["1943", "1944", "1945", "1946"],
        "answer": 3
    },
    {
        "q": "What is the chemical symbol for water?",
        "options": ["H2O", "CO2", "NaCl", "O2"],
        "answer": 1
    },
    {
        "q": "How many sides does a hexagon have?",
        "options": ["5", "6", "7", "8"],
        "answer": 2
    },
    {
        "q": "What is the smallest prime number?",
        "options": ["0", "1", "2", "3"],
        "answer": 3
    },
    {
        "q": "Which planet has the most moons?",
        "options": ["Jupiter", "Saturn", "Uranus", "Neptune"],
        "answer": 2
    },
    {
        "q": "What element does 'O' represent?",
        "options": ["Gold", "Osmium", "Oxygen", "Oganesson"],
        "answer": 3
    },
    {
        "q": "What is the capital of Japan?",
        "options": ["Seoul", "Beijing", "Tokyo", "Bangkok"],
        "answer": 3
    },
    {
        "q": "How many colors are in a rainbow?",
        "options": ["5", "6", "7", "8"],
        "answer": 3
    },
    {
        "q": "What is the largest desert?",
        "options": ["Sahara", "Arabian", "Antarctic", "Gobi"],
        "answer": 3
    },
    {
        "q": "Who painted the Mona Lisa?",
        "options": ["Van Gogh", "Picasso", "Da Vinci", "Monet"],
        "answer": 3
    },
    {
        "q": "What is the boiling point of water in Celsius?",
        "options": ["90", "100", "110", "120"],
        "answer": 2
    },
]


@ghost.command(name="trivia", description="Play a trivia game!", usage="")
async def trivia(ctx):
    if ctx.channel.id in active_trivia:
        await ctx.send("A trivia question is already active in this channel!")
        return

    q = random.choice(questions)
    active_trivia.add(ctx.channel.id)

    options_text = "\n".join(f"  {i}. {opt}" for i, opt in enumerate(q["options"], 1))
    await ctx.send(
        f"**Trivia Time!**\n\n"
        f"{q['q']}\n\n"
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
                f"**Correct!** `{q['options'][q['answer']-1]}` is the right answer.\n"
                f"Score: {trivia_scores[uid]}"
            )
        else:
            await ctx.send(
                f"**Wrong!** The answer was `{q['options'][q['answer']-1]}`."
            )
    except asyncio.TimeoutError:
        await ctx.send(f"**Time's up!** The answer was `{q['options'][q['answer']-1]}`.")
    finally:
        active_trivia.discard(ctx.channel.id)


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
