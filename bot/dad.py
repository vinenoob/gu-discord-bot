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