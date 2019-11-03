from urllib import request
import json

toWatch = ["i am", "i'm", "im"] #all the things to respond to
def daddy(message :str):
    dadMessage = ""
    for watch in toWatch:
        if watch in message.lower(): #if we find what we are looking for
            start = message.find(watch) #find where the daddism starts
            name = message[start+len(watch)+1:] #find the name of the idiot who dared say "I am" or similar
            dadMessage = "Hi " + name + ", I'm dad!"
            return (True, dadMessage)
    return (False, dadMessage)

jokeApi = "https://us-central1-dadsofunny.cloudfunctions.net/DadJokes/random/jokes"
def getDadJoke():
    dadJson = json.loads(request.urlopen(jokeApi).read().decode())
    dadJoke = dadJson['setup'] + "\n"
    dadJoke += dadJson['punchline']
    return dadJoke