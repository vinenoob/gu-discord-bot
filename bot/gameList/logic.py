import os
fileLoc = "bot\\gameList\\"

def addGameToFile(file, game :str):
    file.write(game + "\n")

def addGame(person :str, game :str):
    fileName = fileLoc + person + ".txt"
    with open(fileName, "a+") as file:
        file.write(game + "\n")

# def addGames(person: str, games :list):
#     fileName = fileLoc + person + ".txt"
#     with open(fileName, "a+") as gamesFile:
#         for game in games:
#             addGame(gamesFile, game)

def gameList(person :str):
    fileName = fileLoc + person + ".txt"
    games = ""
    with open(fileName, "r") as gamesFile:
        for line in gamesFile:
            games += line
    return games

def commonGames(people :list):
    gamesInCommon = {""}
    firstPerson = True
    for person in people:
        fileName = fileLoc + person + ".txt"
        personGames = {""}
        personGames.clear()
        with open(fileName, "r") as gamesFile:
            for line in gamesFile:
                if line[len(line)-1:] == "\n":
                    personGames.add(line.lower()[:len(line)-1]) #set lower, delete newline
                else:
                    personGames.add(line.lower())
        if firstPerson:
            gamesInCommon = personGames
            firstPerson = False
        else:
            gamesInCommon = gamesInCommon.intersection(personGames)
    return str(gamesInCommon)
