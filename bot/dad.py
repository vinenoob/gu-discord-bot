
toWatch = ["i am", "i'm", "im"]
def daddy(message :str):
    dadMessage = ""
    for watch in toWatch:
        if watch in message.lower():
            start = message.find(watch)
            name = message[start+len(watch)+1:]
            dadMessage = "Hi " + name + ", I'm dad!"
            return (True, dadMessage)
    return (False, dadMessage)