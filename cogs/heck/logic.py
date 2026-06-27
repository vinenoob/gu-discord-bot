import random
from watch_utils import find_watch_word

HECK_LIST = ["heck", "hell", "darn", "david", "heckin", "fack", "scheiss", "fetch", "fetching", "fetchin", "dang", "shrimp", "johnathan", "livvy", "bathroom"] #all the things to respond to
def heckin(message: str):
    indx, _ = find_watch_word(message, HECK_LIST)
    if indx != -1:
        return True, "Not in my christian minecraft server :sunglasses: "
    return False, ""

YOUR_SPELLINGS = ["your", "youre"]
YOUR_LIST = ["your", "you're"]
def your(message: str):
    for watch in YOUR_LIST:
        for word in message.split():
            if watch != word.lower():
                continue
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

isThisTrueWatchlist = ["true", "real", "what do you think", "false", "verify", "correct"]
# response -> weight (higher weight = picked more often)
responses = {
    "yeah": 10,
    "nah": 2,
    "Here is a useful resource: https://www.google.com": 1,
    "*censored*": 1,
    "ask grok": 1,
    "I'm not allowed to teach you how to make drugs": 1,
}

def isThisTrue(message: str):
    isMatch = False
    for word in isThisTrueWatchlist:
        if word in message.lower():
            isMatch = True
            break
    if not isMatch:
        return False, ""

    response = random.choices(list(responses.keys()), weights=list(responses.values()))[0]
    return True, response


if __name__ == "__main__":
    for i in range(100):
        print(your("your"))