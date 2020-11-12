from urllib import request
import json

#TODO: consider making the dad logic a function for both dad and heck. Dad can handle multiword watches

toWatch = ["heck", "hell", "darn", "david", "heckin", "fack", "scheiss",] #all the things to respond to
def heckin(message :str):
    holy = ""
    for watch in toWatch: #for each word in our watch list
        for word in message.split():
            if watch == word.lower(): #if we find what we are looking for
                holy = "Not in my christian minecraft server :sunglasses: "
                return (True, holy)
    return (False, holy)