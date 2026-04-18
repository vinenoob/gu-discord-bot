import requests
import json
import random
from watch_utils import find_watch_word

toWatch = ["i am", "i\u0027m", "im", "i be"] #all the things to respond to
# i\u0027m uses an explicit escape so editors can't silently replace ' with a curly quote,
# which would break matching after normalization.
daddyOn = True

alphanumeric = "123456789abcdefgh"
# Maps curly/fancy apostrophe variants to a plain ASCII apostrophe (U+0027) so all
# of them match the "i'm" entry above. Uses integer codepoints to avoid the same
# editor-encoding problem.
_ODD_APOSTROPHES = str.maketrans({0x2018: 0x27, 0x2019: 0x27, 0x02BC: 0x27, 0xFF07: 0x27})

def daddy(message :str, percentChance :int = 100):
    if not daddyOn:
        return ""

    message = message.translate(_ODD_APOSTROPHES)
    indx, watch = find_watch_word(message, toWatch)
    if indx == -1:
        return ""

    end_pos = indx + len(watch)
    # must be followed by a space and a name
    if end_pos >= len(message) or message[end_pos] != " ":
        return ""

    name = message[end_pos + 1:]
    randomNum = random.randint(0, 100)
    if randomNum > percentChance:
        return ""

    return f"Hi {name}, I’m dad!"

def turnDaddyOn():
    global daddyOn
    daddyOn = True

def turnDaddyOff():
    global daddyOn
    daddyOn = False # :(

# jokeApi = "https://us-central1-dadsofunny.cloudfunctions.net/DadJokes/random/jokes"
jokeApi = "https://icanhazdadjoke.com/"

def getDadJoke():
    dadJson = json.loads(requests.get(jokeApi, headers={"Accept": "application/json"}).text)
    return dadJson['joke']