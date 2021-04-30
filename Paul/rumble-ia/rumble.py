# import numpy as np
import random as rd

##### CONSTANTS #####


##### FUNCTIONS #####


def generateGame(numberOfPlayers):
    """initiates the game: create a random room disposition, a random repartition of characters in the rooms and a random repartions of characters among the players"""
    alivePlayersList = list(range(1, numberOfPlayers + 1))
    aliveCharactersList = list(range(1, (numberOfPlayers * 2) + 1))
    playOrder = list(range(1, (numberOfPlayers) + 1))
    characterRepartition = list(
        map(lambda el: [el], range(1, (numberOfPlayers * 2) + 1)))
    # roomDisposition = [0, 0, 0, 0] + list(range(1, (numberOfPlayers * 2) + 1))
    roomDisposition = list(range(1, (numberOfPlayers * 2) + 1))

    rd.shuffle(playOrder)
    rd.shuffle(roomDisposition)
    rd.shuffle(characterRepartition)

    playerTokensList = allocateTokens(numberOfPlayers)

    return alivePlayersList, aliveCharactersList, playOrder, characterRepartition, roomDisposition, playerTokensList


def allocateTokens(numberOfPlayers):
    """Generates a list of size [number of players] which contains tuples. Each tupple contains 2 token id. Player #X possesses the tokens stored in the list at index X - 1"""
    tokenList = list(range(1, (numberOfPlayers * 2) + 1))
    playerTokensList = []

    for index in range(numberOfPlayers):
        selectedTokens = rd.sample(tokenList, 2)
        playerTokensList.append([selectedTokens[0],
                                 selectedTokens[1]])
        tokenList.remove(selectedTokens[0])
        tokenList.remove(selectedTokens[1])

    return playerTokensList


def searchKills(playerID):
    """returns the position in  of all rooms containing more than """
    killPossibilities = []
    for room, roomIndex in zip(characterRepartition, list(range(0, len(characterRepartition)))):
        list1 = list(map(lambda element: element in room,
                         playerTokensList[playerID - 1]))
        if len(room) > 2 or (len(room) > 1 and list1 != [True, True]):
            killPossibilities.append(roomIndex)
    return killPossibilities


def randomKill(killer, roomSelection):
    """TODO create copy of room, remove player tokens and then choose instead randomly choosing and then rerolling """
    selectedRoomIndex = rd.sample(roomSelection, 1)[0]
    killedCharacter = rd.sample(characterRepartition[selectedRoomIndex], 1)[0]

    if killedCharacter in playerTokensList[killer - 1]:
        return randomKill(killer, roomSelection)
    for room in characterRepartition:
        if killedCharacter in room:
            room.remove(killedCharacter)
    deadCharacters.append(killedCharacter)

    aliveCharactersList.remove(killedCharacter)

    for player in range(0, numberOfPlayers):
        if (playerTokensList[player][0] in deadCharacters and playerTokensList[player][1] in deadCharacters and player + 1 in alivePlayersList):
            alivePlayersList.remove(player + 1)


def searchMoves():
    """returns an array containing the position in the characterRepartition array of all rooms containing only one character"""
    movePossibilities = []

    for room, roomIndex in zip(characterRepartition, list(range(0, len(characterRepartition)))):
        if len(room) == 1:
            movePossibilities.append(roomIndex)

    return movePossibilities


def randomMove(roomSelection):
    selectedRoomIndex = rd.sample(roomSelection, 1)[0]
    backOrForth = rd.sample([-1, 1], 1)[0]
    if (selectedRoomIndex == 0 and backOrForth == -1) or (selectedRoomIndex == ((numberOfPlayers * 2) - 1) and backOrForth == 1):
        backOrForth *= -1
    characterRepartition[selectedRoomIndex +
                         backOrForth].append(characterRepartition[selectedRoomIndex][0])
    characterRepartition[selectedRoomIndex].remove(
        characterRepartition[selectedRoomIndex][0])
    return 'break'


def chooseAction():
    print('in chooseAction')


##### MAIN #####

numberOfPlayers = int(input("Number of players (2 to 6): "))
numberOfRounds = 1000

for round in range(1, numberOfRounds + 1):
    # seed = 2470
    # seed = n
    #rng = rd.seed(seed)
    print('numberOfTries =', round)
    gameInfo = generateGame(numberOfPlayers)


    alivePlayersList = gameInfo[0]
    aliveCharactersList = gameInfo[1]
    playOrder = gameInfo[2]
    characterRepartition = gameInfo[3]
    roomDisposition = gameInfo[4]
    playerTokensList = gameInfo[5]

    deadCharacters = []
    numberOfTurns = 0

    while len(aliveCharactersList) > 1 and len(alivePlayersList) > 1:
        numberOfTurns += 1
        for playerID in playOrder:
            if len(aliveCharactersList) == 1 or len(alivePlayersList) == 1:
                break
            movePossibilities = searchMoves()
            killPossibilities = searchKills(playerID)
            if len(killPossibilities) == 0 and len(movePossibilities) != 0:
                randomMove(movePossibilities)
            elif len(movePossibilities) == 0 and len(killPossibilities) != 0:
                randomKill(playerID, killPossibilities)
            else:
                killOrMove = rd.randint(0, 1)
                if killOrMove == 0:
                    randomKill(playerID, killPossibilities)
                else:
                    randomMove(movePossibilities)

    print('final characterRepartition =', characterRepartition,
          'numberOfTurns =', numberOfTurns)
