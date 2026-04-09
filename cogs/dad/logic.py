import requests
import json
import random
from watch_utils import find_watch_word

toWatch = ["i am", "i’m", "i’m", "im", "i be"] #all the things to respond to
daddyOn = True

alphanumeric = "123456789abcdefgh"

def daddy(message :str, percentChance :int = 100):
    if not daddyOn:
        return ""

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

    return f"Hi {name}, I’m dad! (debug)"

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