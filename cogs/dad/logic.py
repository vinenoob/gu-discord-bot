import requests
import json
import random

toWatch = ["i am", "i'm", "i’m", "im", "i be"] #all the things to respond to
daddyOn = True

#TODO: consider making the dad logic a function for both dad and heck. Dad can handle multiword watches

def daddy(message :str, percentChance :int = 100):
    if not daddyOn:
        return (False, "")

    for watchWord in toWatch:
        indx = message.lower().find(watchWord.lower())
        if indx == -1: #if we didn't found the word
            continue

        #check if the character after the watch word is a space, helping to indicate if it is it's own 
        # word/phrase, and not apart of another word ie "i believe" contains "i be" but we don't want
        # to catch it
        if message[indx + len(watchWord)] != " ": 
            continue


        name = ""
        found = False
        if indx == 0: 
            #we have found the word and it is the first word in the message
            found = True
            name = message[indx + len(watchWord) + 1:] # +1     ecasue we want to exclude the space after the watc
        elif message[indx - 1] == " ": #if it is not the first word in the message
            #we have found the word and the previous character is a space, therefor the word is not just a substring
            found = True
            name = message[indx + len(watchWord) + 1:] # +1 becasue we want to exclude the space after the watch

        randomNum = random.randint(0, 100)
        if found and randomNum > percentChance: #if we didn't hit the chance threshold, we won't respond
            return (False, "")
        
        return (found, f"Hi {name}, I'm dad!")
        
    return (False, "")

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