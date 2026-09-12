import random


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
        await ctx.send("Provide text or reply to a message: `.mock hello world`")
        return
    await ctx.send(to_spongebob(text))


@ghost.command(name="mockify", description="Same as mock.", usage="[text]")
async def mockify(ctx, *, text=None):
    await mock(ctx, text=text)
