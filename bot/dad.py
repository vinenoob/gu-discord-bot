from urllib import request
import json

toWatch = ["i am ", "i'm ", "im ", "i be "] #all the things to respond to
daddyOn = True
def daddy(message :str):
    if daddyOn:
        dadMessage = ""
        for watch in toWatch: #if we can't find any watchwords it will skip the contents of the loop
            if watch in message.lower(): #if we find what we are looking for
                start = message.lower().find(watch) #find where the daddism starts
                name = message[start+len(watch):] #find the name of the idiot who dared say "I am" or similar
                dadMessage = "Hi " + name + ", I'm dad!"
                return (True, dadMessage)
    return (False, "")

def turnDaddyOn():
    global daddyOn
    daddyOn = True

def turnDaddyOff():
    global daddyOn
    daddyOn = False

jokeApi = "https://us-central1-dadsofunny.cloudfunctions.net/DadJokes/random/jokes"
def getDadJoke():
    dadJson = json.loads(request.urlopen(jokeApi).read().decode())
    dadJoke = dadJson['setup'] + "\n"
    dadJoke += dadJson['punchline']
    return dadJoke