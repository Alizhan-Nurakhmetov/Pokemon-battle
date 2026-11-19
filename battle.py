import json
from functools import lru_cache
from random import choice
from urllib.request import urlopen, Request

def starters():
    """Return the three starter names"""
    return ("bulbasaur", "charmander", "squirtle")
@lru_cache(maxsize=3)
def get_pokemon(name):
    """Get the name, type and HP"""
    url = f"https://pokeapi.co/api/v2/pokemon/{name}/"
    request = Request(url, headers = {"User-Agent": "PokemonBattle/1.0"})
    with urlopen(request, timeout = 5) as responce:
        data= json.load(responce)
    kind = data["types"][0]["type"]["name"]
    for stat in data["stats"]:
        if stat["stat"]["name"] == "hp":
            return {"name": data["name"].title(), "type":kind, "hp": stat["base_stat"]}
    raise ValueError("PokeAPI did not return HP")

def start(name):
    """Set up a battle"""
    rivals = list(starters())
    if name not in rivals:
        raise ValueError("Choose one of the three starters")
    rivals.remove(name)
    player = get_pokemon(name)
    rival = get_pokemon(choice(rivals))
    return {"fighters": [player, rival], "hp": [player["hp"], rival["hp"]]}

def damage (attack, attacker, defender):
    """The damage of one attack"""
    if attack == "Basic":
        return 10
    strong = {("grass", "water"), ("water", "fire"), ("fire", "grass")}
    if (attacker["type"], defender["type"]) in strong:
        return 16
    return 6

def play(battle, attack):
    """Play a turn and return a message"""
    attacks = ("Basic", "Type")
    if not battle or 0 in battle["hp"]:
        raise ValueError("Start a new battle first")
    if attack not in attacks:
        raise ValueError("Choose Basic or Type")
    player, rival = battle["fighters"]
    hp = battle["hp"].copy()
    hit = damage(attack, player, rival)
    hp[1] = max(0, hp[1] - hit)
    message = f"{player['name']} dealt {hit} damage"
    if hp[1] == 0:
        message += ". You win!"
    else:
        reply = choice(attacks)
        hit = damage (reply, rival, player)
        hp[0] = max(0, hp[0] - hit)
        message += f" {rival['name']} dealt {hit} damage"
        if hp[0] == 0:
            message += ". You lose!"
    return {"fighters": battle["fighters"], "hp": hp}, message

