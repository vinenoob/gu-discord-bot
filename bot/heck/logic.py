from urllib import request
import random
import json

#TODO: consider making the dad logic a function for both dad and heck. Dad can handle multiword watches

HECK_LIST = ["heck", "hell", "darn", "david", "heckin", "fack", "scheiss", "fetch", "fetching", "fetchin", "dang", "shrimp", "johnathan"] #all the things to respond to
def heckin(message: str):
    holy = ""
    for watch in HECK_LIST: #for each word in our watch list
        for word in message.split():
            if watch == word.lower(): #if we find what we are looking for
                holy = "Not in my christian minecraft server :sunglasses: "
                return True, holy
    return False, holy

YOUR_SPELLINGS = ["your", "youre"]
YOUR_LIST = ["your", "you're"]
def your(message: str):
    for watch in YOUR_LIST:
        for word in message.split():
            if watch == word.lower():
                yorResponse = list(random.choice(YOUR_SPELLINGS))
                addedApostrophe = False
                for i, letter in enumerate(yorResponse):
                    print(letter)
                    if not addedApostrophe:
                        appostropheRNG = random.randint(i, len(yorResponse)-1)
                        if appostropheRNG == i:
                            yorResponse.insert(i, "'")
                            addedApostrophe = True

                    deleteRNG = random.randint(0, 6)
                    if deleteRNG == 0:
                        yorResponse.pop(i)
                        
                scrambleRNG = random.randint(0, 1)
                if scrambleRNG == 0:
                    firstLetterPos = random.randint(0, len(yorResponse)-1)
                    secondLetterPos = firstLetterPos + 1
                    if secondLetterPos == len(yorResponse):
                        secondLetterPos = firstLetterPos - 1
                    yorResponse[firstLetterPos], yorResponse[secondLetterPos] = yorResponse[secondLetterPos], yorResponse[firstLetterPos]
                if word[0].isupper():
                    yorResponse[0] = yorResponse[0].upper()
                return True, "".join(yorResponse) + "*"
    return False, ""
if __name__ == "__main__":
    for i in range(100):
        print(your("your"))