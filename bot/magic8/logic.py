import random

responses = ["no", "yes", "dave", "i'm busy"]

def magic8() -> str:
    rand = random.choice(responses)
    print(rand)
    return rand