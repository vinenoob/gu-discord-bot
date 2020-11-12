from urllib import request
import json

toWatch = ["i am", "i'm", "im", "i be"] #all the things to respond to
daddyOn = True

#TODO: consider making the dad logic a function for both dad and heck. Dad can handle multiword watches

def daddy(message: str):
    if daddyOn:
        if message.lower() == "hi dad":
            return (True, "heck the police")

        messageWords = message.split()
        for i in range(len(messageWords)):
            for watchWord in toWatch:
                match = True #we are going to prove if the watchWord is in the message
                watchWordWords = watchWord.split()
                for j in range(len(watchWordWords)):
                    try:
                        if watchWordWords[j] != messageWords[i + j].lower(): #compare watchWordWords to the messageWords, trying to prove they don't match
                            match = False 
                            break
                    except IndexError:
                        return (False, "")
                if match:
                    start = message.lower().find(watchWord) #find where the daddism starts
                    name = message[start+len(watchWord)+1:] #find the name of the idiot who dared say "I am" or similar
                    dadMessage = "Hi " + name + ", I'm dad!"
                    return (True, dadMessage)
        return (False, "")


def daddy2(message :str):
    if daddyOn:
        dadMessage = ""
        for watch in toWatch: #if we can't find any watchwords it will skip the contents of the loop
            for word in message.split(): #for each word in the message
                for subWord in watch.split(): #to deal with split thing ie "I am"
                    if subword == word.lower():
                        pass
                # if watch == word.lower(): #if we find what we are looking for
                #     start = message.lower().find(watch) #find where the daddism starts
                #     name = message[start+len(watch):] #find the name of the idiot who dared say "I am" or similar
                #     dadMessage = "Hi " + name + ", I'm dad!"
                #     return (True, dadMessage)
        if message.lower() == "hi dad":
            return (True, "heck the police")
    return (False, "")

def turnDaddyOn():
    global daddyOn
    daddyOn = True

def turnDaddyOff():
    global daddyOn
    daddyOn = False # :(

jokeApi = "https://us-central1-dadsofunny.cloudfunctions.net/DadJokes/random/jokes"
def getDadJoke():
    dadJson = json.loads(request.urlopen(jokeApi).read().decode())
    dadJoke = dadJson['setup'] + "\n"
    dadJoke += dadJson['punchline']
    return dadJoke