from urllib import request
import json

toWatch = ["heck", "hell", "darn",] #all the things to respond to
def daddy(message :str):
    holy = ""
    for watch in toWatch:
        if watch in message.lower(): #if we find what we are looking for
            holy = "Not in my christian minecraft server :sunglasses: "
            return (True, holy)
    return (False, holy)