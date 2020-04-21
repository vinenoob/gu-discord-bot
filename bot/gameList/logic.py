import os
fileLoc = os.path.join(os.getcwd(), 'bot', 'gameList')

def addGame(person :str, game :str):
    fileName = os.path.join(fileLoc, person + ".txt")
    with open(fileName, "a+") as gamesFile:
        gamesFile.write(game + "\n")

def removeGame(person :str, game :str):
    fileName = os.path.join(fileLoc, person + ".txt")
    games = ""
    found_game = False
    with open(fileName, "r") as gamesFile:
        for line in gamesFile:
            if line.replace("\n", "") != game:
                games += line
            else:
                found_game = True
    with open(fileName, "w") as gamesFile:
        gamesFile.write(games)
    if(found_game):
        return True
    else:
        return False


def gameList(person :str):
    fileName = os.path.join(fileLoc, person + ".txt")
    games = ""
    with open(fileName, "r") as gamesFile:
        for line in gamesFile:
            games += line
    return games

def commonGames(people :list):
    gamesInCommon = {""}
    firstPerson = True
    for person in people:
        fileName = os.path.join(fileLoc, person + ".txt")
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
    return list(gamesInCommon)
