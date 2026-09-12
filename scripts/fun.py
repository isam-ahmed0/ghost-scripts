import random
import asyncio

PREFIX = ghost.command_prefix


# ─────────────────────────────────────────────
#  Fortune
# ─────────────────────────────────────────────

fortunes = [
    "A beautiful, smart, and loving person will come into your life.",
    "A faithful friend is a strong defense.",
    "A fresh start will put you on your way.",
    "A golden egg of opportunity falls into your lap this month.",
    "A good time to finish up old tasks.",
    "A lifetime of happiness lies ahead of you.",
    "A light heart carries you through all the hard times.",
    "A new perspective will come with the new year.",
    "A smooth sea never made a skilled sailor.",
    "A stranger will soon become a very important friend.",
    "All the effort you are putting into your career will pay off.",
    "Believe in yourself and others will too.",
    "Changes in your life today will lead to greater contentment.",
    "Courage is not the absence of fear; it is acting in spite of it.",
    "Disregard the last fortune and focus on this one.",
    "Do not make extra work for yourself.",
    "During the next two months, you will receive good news.",
    "Every day in your life is a special occasion.",
    "Failure is the chance to do better next time.",
    "Fortune favors the brave.",
    "From small beginnings come great things.",
    "Good news will come to you by mail.",
    "Happiness begins with facing life with a smile and a wink.",
    "Hard work pays off in the future, however laziness pays off now.",
    "Have you tried turning it off and on again?",
    "He who laughs at himself never runs out of things to laugh at.",
    "If you keep your feet on the ground, you will bump your head.",
    "It is always the simple that produces the marvelous.",
    "It is better to be a failure at something you love than a success at something you hate.",
    "Nothing is impossible to a willing heart.",
    "Observe your surroundings. They may hold the answer.",
    "Once in a while, you really need to take a break and be grateful for what you have.",
    "Others admire your independent spirit.",
    "Sail swiftly on the waters of life.",
    "The best prediction of the future is to create it.",
]


@ghost.command(name="fortune", description="Get your fortune told.", usage="")
async def fortune(ctx):
    await ctx.send(f"**Fortune:** {random.choice(fortunes)}")


# ─────────────────────────────────────────────
#  Mock
# ─────────────────────────────────────────────

def to_spongebob(text):
    result = []
    upper = True
    for char in text:
        if char.isalpha():
            result.append(char.upper() if upper else char.lower())
            upper = not upper
        else:
            result.append(char)
    return "".join(result)


@ghost.command(name="mock", description="MoCKifY TeXt. Reply to a message or provide text.", usage="[text]")
async def mock(ctx, *, text=None):
    if text is None and ctx.message.reference:
        ref = ctx.message.reference.resolved
        if ref and ref.author:
            text = ref.content
    if not text:
        await ctx.send(f"Provide text or reply to a message: `{PREFIX}mock hello world`")
        return
    await ctx.send(to_spongebob(text))


@ghost.command(name="mockify", description="Same as mock.", usage="[text]")
async def mockify(ctx, *, text=None):
    await mock(ctx, text=text)


# ─────────────────────────────────────────────
#  Autocorrect
# ─────────────────────────────────────────────

corrections = {
    "hello": "halibut", "hi": "hippopotamus", "yes": "yeast", "no": "noodle",
    "good": "guacamole", "bad": "baguette", "the": "thermos", "is": "igloo",
    "are": "armadillo", "was": "walrus", "you": "yourself", "me": "mango",
    "my": "mayonnaise", "your": "yogurt", "what": "watermelon", "why": "waffle",
    "how": "hologram", "when": "wensleydale", "where": "worcestershire",
    "who": "horseshoe", "okay": "okra", "thanks": "tangerines", "please": "pineapple",
    "sorry": "spaghetti", "love": "lasagna", "hate": "hashbrown", "want": "wonton",
    "need": "nectarine", "go": "gnocchi", "come": "calamari", "run": "rhubarb",
    "walk": "waffle", "eat": "eggplant", "drink": "dragonfruit", "sleep": "souffle",
    "work": "wonton", "help": "hummus", "friend": "focaccia", "dog": "dumpling",
    "cat": "cannoli", "man": "manchego", "woman": "wasabi", "girl": "gelato",
    "boy": "brioche", "people": "porridge", "think": "tempura", "know": "kumquat",
    "give": "guava", "take": "tiramisu", "make": "mochi", "do": "doughnut",
    "have": "hazelnut", "like": "linguine", "say": "seitan", "get": "ginger",
    "see": "seaweed", "look": "lemon", "feel": "fennel", "tell": "tahini",
    "ask": "artichoke", "put": "pudding", "keep": "kombucha", "start": "starfruit",
    "show": "shallot", "try": "turnip", "must": "mushroom", "very": "vanilla",
    "much": "mustard", "with": "waffle", "from": "fromage", "about": "avocado",
    "would": "wonton", "could": "couscous", "should": "shortbread", "will": "willow",
    "can": "cantaloupe", "just": "jalapeno", "really": "ravioli", "also": "alfredo",
    "because": "brioche", "before": "baguette", "after": "arugula", "other": "oatmeal",
    "through": "tempura", "some": "samosa", "more": "mozzarella", "than": "tahini",
    "most": "marzipan", "only": "oregano", "over": "oatmeal", "such": "sundae",
    "back": "biscuit", "well": "wonton", "even": "edamame", "still": "steak",
    "down": "dumpling", "being": "brioche", "same": "sashimi", "own": "onion",
    "too": "tofu", "now": "naan", "new": "noodles", "way": "waffle",
    "use": "udon", "her": "hummus", "him": "hummus", "his": "hazelnut",
    "our": "orange", "out": "omelette", "for": "fondue", "and": "andouille",
    "but": "butter", "not": "nougat", "all": "alfredo", "any": "anchovy",
    "many": "marmalade", "may": "mayo", "these": "sesame", "those": "tofu",
    "two": "tofu", "one": "onion", "first": "focaccia",
}


@ghost.command(name="autocorrect", description="'Correct' text to food names.", usage="[text]")
async def autocorrect(ctx, *, text=None):
    if not text:
        await ctx.send(f"Provide text: `{PREFIX}autocorrect I love you`")
        return

    result = []
    changed = False
    for word in text.split():
        lower = word.lower().strip(".,!?;:'\"")
        if lower in corrections:
            result.append(corrections[lower])
            changed = True
        else:
            result.append(word)

    if changed:
        await ctx.send(f"**Autocorrected:** {' '.join(result)}")
    else:
        await ctx.send("No corrections needed! Your text was perfect.")


# ─────────────────────────────────────────────
#  Ghost ping
# ─────────────────────────────────────────────

@ghost.command(name="ghostping", description="Send a fake ghost ping that auto-deletes.", usage="[@user]")
async def ghostping(ctx, member: discord.Member = None):
    if member is None:
        await ctx.send(f"Mention someone: `{PREFIX}ghostping @user`")
        return

    msg = await ctx.send(f"**BOO!** {member.mention}")
    await asyncio.sleep(1)
    try:
        await msg.delete()
    except Exception:
        pass

    try:
        await ctx.message.delete()
    except Exception:
        pass


# ─────────────────────────────────────────────
#  Typing troll
# ─────────────────────────────────────────────

@ghost.command(name="typingtroll", description="Show typing indicator for a long time, then do nothing.", usage="[@user]")
async def typingtroll(ctx, member: discord.Member = None):
    if member is None:
        await ctx.send(f"Mention someone: `{PREFIX}typingtroll @user`")
        return

    duration = random.randint(10, 30)
    await ctx.send(f"Typing to {member.mention}...")

    async with ctx.typing():
        await asyncio.sleep(duration)

    responses = ["nvm", "...", "nevermind", "I forgot what I was gonna say", "jk", "actually nevermind", "lol nvm"]
    await ctx.send(random.choice(responses))


# ─────────────────────────────────────────────
#  Compliment bomb
# ─────────────────────────────────────────────

compliments = [
    "You're like a ray of sunshine on a cloudy day.",
    "Your smile is contagious.",
    "You have the best laugh.",
    "You light up the room.",
    "You have a great sense of humor.",
    "You're really strong.",
    "You have the best style.",
    "You're an awesome friend.",
    "You're a great listener.",
    "You bring out the best in other people.",
    "You're incredible and irreplaceable.",
    "You make the world a better place.",
    "You're making a difference.",
    "You're worth far more than you know.",
    "You always know exactly what to say.",
    "You're one of a kind.",
    "You're so thoughtful.",
    "You're destined for greatness.",
    "You are enough just as you are.",
    "You have the purest heart.",
    "You're an inspiration.",
    "You're so talented.",
    "You're a true original.",
    "You're so fun to be around.",
    "Your creativity is inspiring.",
]


@ghost.command(name="complimentbomb", description="Send several compliments to a user.", usage="[@user]", aliases=["compliments"])
async def complimentbomb(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author

    for _ in range(3):
        await ctx.send(f"{member.mention} {random.choice(compliments)}")

    await ctx.send(f"{ctx.author.display_name} complimented {member.display_name} 3 times!")