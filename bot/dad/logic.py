from typing import Tuple
# from urllib import request
import requests
import json
import re

toWatch = ["i am", "i'm", "im", "i be"] #all the things to respond to
daddyOn = True

#TODO: consider making the dad logic a function for both dad and heck. Dad can handle multiword watches

def daddy(message :str):
    # message = message.lower()
    if daddyOn:
        for watchWord in toWatch:
            indx = message.lower().find(watchWord.lower())
            if indx != -1: #if we found the word
                if message[indx + len(watchWord)] == " ": 
                    #check if the character after the watch word is a space, helping to indicate if it is it's own 
                    # word/phrase, and not apart of another word ie "i believe" contains "i be" but we don't want
                    # to catch it
                    if indx != 0: #if it is not the first word in the message
                        if message[indx - 1] == " ": 
                            #we have found the word and the previous character is a space, therefor the word is not just a substring
                            name = message[indx + len(watchWord) + 1:] # +1 becasue we want to exclude the space after the watch
                            return (True, f"Hi {name}, I'm dad!")
                    else: 
                        #we have found the word and it is the first word in the message
                        name = message[indx + len(watchWord) + 1:] # +1 becasue we want to exclude the space after the watch
                        return (True, f"Hi {name}, I'm dad!")
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