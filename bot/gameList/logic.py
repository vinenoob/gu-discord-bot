import os
fileLoc = "gu-discord-bot\\bot\\gameList\\"
def addGame(person :str, game :str):
    fileName = fileLoc + person + ".txt"
    with open(fileName, "a+") as file:
        file.write(game + "\n")

def gameList(person :str):
    fileName = fileLoc + person + ".txt"
    games = ""
    with open(fileName, "r") as gamesFile:
        for line in gamesFile:
            games += line
            
    return games