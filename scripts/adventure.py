import random

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
            "text": "The passage leads to aoblin camp. A goblin guard spots you!",
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
                "2": {"text": "Try to open chest anyway", "next": "open_chest"},
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
        await ctx.send("An adventure is already active! Use `.choice [1-3]`")
        return

    adventure_games[ctx.channel.id] = {
        "hp": 100,
        "gold": 0,
        "items": [],
        "scene": "start",
    }

    scenes = get_scenes()
    scene = scenes["start"]

    choices_text = "\n".join(f"  {k}. {v['text']}" for k, v in scene["choices"].items())
    await ctx.send(
        f"**Dungeon Adventure!**\n\n"
        f"{scene['text']}\n\n"
        f"```\n{choices_text}\n```\n"
        f"HP: 100 | Gold: 0\n"
        f"Choose with `.choice [number]`"
    )


@ghost.command(name="choice", description="Make a choice in your adventure.", usage="[1-3]")
async def choice(ctx, num=None):
    if ctx.channel.id not in adventure_games:
        await ctx.send("No active adventure. Start one with `.adventure`")
        return

    if num is None or num not in ("1", "2", "3"):
        await ctx.send("Pick a choice: `.choice 1`")
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

    next_scene = chosen["next"]
    next_scene_data = scenes[next_scene]

    game["gold"] += next_scene_data.get("gold", 0)
    game["items"].extend(next_scene_data.get("items", []))
    game["scene"] = next_scene

    if hp_cost > 0:
        await ctx.send(f"**-{hp_cost} HP** from the battle!")

    text = next_scene_data["text"]
    items_str = f"\nItems: {', '.join(game['items'])}" if game["items"] else ""

    if next_scene_data.get("end"):
        await ctx.send(
            f"**Adventure Complete!**\n\n{text}\n\n"
            f"Final HP: {game['hp']} | Gold: {game['gold']}{items_str}"
        )
        del adventure_games[ctx.channel.id]
        return

    choices = next_scene_data.get("choices", {})
    if not choices:
        await ctx.send(
            f"{text}\n\nFinal HP: {game['hp']} | Gold: {game['gold']}{items_str}"
        )
        del adventure_games[ctx.channel.id]
        return

    choices_text = "\n".join(f"  {k}. {v['text']}" for k, v in choices.items())
    await ctx.send(
        f"{text}\n\n"
        f"```\n{choices_text}\n```\n"
        f"HP: {game['hp']} | Gold: {game['gold']}{items_str}\n"
        f"Choose with `.choice [number]`"
    )
