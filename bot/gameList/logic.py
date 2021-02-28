import os
import typing
fileLoc = os.path.join(os.getcwd(), 'gameList', 'peoples-games')

def getGames(person :str):
    games = []
    fileName = getFileName(person)
    with open(fileName, "a+") as gamesFile: #a+ to create file if the user doesnt have one
        gamesFile.seek(0)
        for line in gamesFile:
            games.append(line.replace("\n", "")) #add games, exclude newline characters
    return games

def getFileName(person :str):
    return os.path.join(fileLoc, person + ".txt")

def addGame(person :str, game :str):
    games = getGames(person)
    if game in games:
        return (False, game + " already in your list!")
    else:
        with open(getFileName(person), "a+") as gamesFile:
            gamesFile.write(game + "\n")
        return (True, "Added " + game)

def removeGame(person :str, gameToRemove :str):
    found_game = False
    games = getGames(person)

    for game in games:
        if game == gameToRemove:
            games.remove(game)
            found_game = True
            break

    with open(getFileName(person), "w") as gamesFile:
        for game in games:
            gamesFile.write(game + "\n")

    return found_game


def gameList(person :str):
    games = ""
    gamesList = getGames(person)
    for game in gamesList:
        games += game + "\n"
    return games

def commonGames(people :typing.List[str]):
    gameSets = []
    for person in people:
        gamesList = getGames(person)
        personGames = set() #this is a set
        for game in gamesList:
            personGames.add(game.lower())
        gameSets.append(personGames)
        
    gamesInCommon = set()
    for i in range(len(gameSets)):
        if i == 0:
            gamesInCommon = gameSets[i]
        else:
            gamesInCommon = gamesInCommon.intersection(gameSets[i])
    return list(gamesInCommon)

if __name__ == "__main__":
    print(commonGames(["vinenoob", "test", "test2"]))