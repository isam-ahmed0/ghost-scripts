import random

compliments = [
    "You're like a ray of sunshine on a cloudy day.",
    "Your smile is contagious.",
    "You have the best laugh.",
    "You light up the room.",
    "You have a great sense of humor.",
    "Being around you is like a happy little vacation.",
    "You have the most contagious smile.",
    "Your eyes are stunning.",
    "You're really strong.",
    "You have the best style.",
    "You're an awesome friend.",
    "You're a great listener.",
    "You bring out the best in other people.",
    "You have the coolest ideas.",
    "You're incredible and irreplaceable.",
    "You're like a human golden retriever - everyone loves you.",
    "You make the world a better place.",
    "You're making a difference.",
    "You're a light in someone's darkness.",
    "You're worth far more than you know.",
    "You always know exactly what to say.",
    "You're braver than you believe.",
    "You're more fun than anyone or anything I know.",
    "You're one of a kind.",
    "You have the greatest ideas.",
    "You're so thoughtful.",
    "You're destined for greatness.",
    "You're a gift to those around you.",
    "You're a ray of sunshine.",
    "You are enough just as you are.",
    "You make me want to be a better person.",
    "You have the purest heart.",
    "You're an inspiration.",
    "You're so talented.",
    "You have impeccable manners.",
    "You're a true original.",
    "You give the best hugs.",
    "You're so fun to be around.",
    "Your creativity is inspiring.",
    "You're a blessing to everyone who knows you.",
]


@ghost.command(name="compliment", description="Send a compliment to a user.", usage="[@user]")
async def compliment(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author

    count = 0
    for _ in range(3):
        c = random.choice(compliments)
        await ctx.send(f"{member.mention} {c}")
        count += 1

    await ctx.send(f"{ctx.author.display_name} complimented {member.display_name} {count} times!")
