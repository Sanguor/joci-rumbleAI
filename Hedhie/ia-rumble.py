import socketio
import random as rd

sio = socketio.Client()

globalBoard = []
globalPawns = []


### AI FUNCTIONS ###

def handleData(data):
    width = data['board']['width']
    height = data['board']['height']
    board = []
    pawns = data['pawns']
    senderId = data['senderId']

    boardData = data['board']['data']
    if len(boardData) != 20:
        for index in range(0, 20 - len(boardData)):
            boardData.append(None)

    for index in range(0, len(boardData)):
        if (index in [0, 5, 10, 15]):
            subArray = []
        subArray.append(boardData[index])
        if (index in [4, 9, 14, 19]):
            board.append(subArray)
    return width, height, board, pawns, senderId


def movePawn(x, y, pawnId):
    for subArray in globalBoard:
        for index in range(0, len(subArray)):
            if subArray[index] != None:
                if pawnId in subArray[index]:
                    subArray[index].remove(pawnId)
    globalBoard[y][x].append(pawnId)


def killPawn(x, y, pawnId):
    globalBoard[y][x].remove(pawnId)


def searchKills():
    """returns the position in  of all rooms containing more than one pawn"""
    killPossibilities = []
    for subArray, subArrayIndex in zip(globalBoard, list(range(0, len(globalBoard)))):
        for room, roomIndex in zip(subArray, list(range(0, len(subArray)))):
            if room != None:
                list1 = list(map(lambda element: element in room, globalPawns))
                if len(room) > 2 or (len(room) > 1 and list1 != [True, True]):
                    killPossibilities.append([roomIndex, subArrayIndex])
    return killPossibilities


def randomKill(roomSelection):
    selectedRoom = rd.sample(roomSelection, 1)[0]
    randomSample = rd.sample(
        globalBoard[selectedRoom[1]][selectedRoom[0]], 2)

    killer = randomSample[0]
    killedCharacter = randomSample[1]

    if killedCharacter in globalPawns:
        return randomKill(roomSelection)

    sio.emit("kill", {'killer': killer, 'killed': killedCharacter})
    return


def searchMoves():
    """returns an array containing the position in the globalBoard array of all rooms containing only one character"""
    movablePawns = []

    for subArray, subArrayIndex in zip(globalBoard, list(range(0, len(globalBoard)))):
        for room, roomIndex in zip(subArray, list(range(0, len(subArray)))):
            if room != None:
                if len(room) == 1:
                    movablePawns.append([room[0], roomIndex, subArrayIndex])

    return movablePawns


def randomMove(pawnSelection):
    selectedPawn = rd.sample(pawnSelection, 1)[0]

    availableSlots = [[selectedPawn[1] - 1, selectedPawn[2]], [selectedPawn[1] + 1, selectedPawn[2]],
                      [selectedPawn[1], selectedPawn[2] - 1], [selectedPawn[1], selectedPawn[2] + 1]]

    selectedDirection = [None, None]
    while (selectedDirection[0] in [None, -1, 5] or selectedDirection[1] in [None, -1, 4] or (globalBoard[selectedDirection[1]][selectedDirection[0]] == None)):
        selectedDirection = rd.sample(availableSlots, 1)[0]

    pawn = selectedPawn[0]
    x = selectedDirection[0]
    y = selectedDirection[1]
    sio.emit("move", {'pawn': pawn, 'destination': {'x': x, 'y': y}})

    return


### SIO FUNCTIONS ###

@sio.event
def connect():
    print('connection established')


@sio.event
def my_message(data):
    print('message received with ', data)
    sio.emit('room', {'roomName': 'rumble'})


@sio.event
def handleStart(data):
    print('dataStart =', data)
    global globalBoard
    global globalPawns
    parsedData = handleData(data)

    width = parsedData[0]
    height = parsedData[1]
    globalBoard = parsedData[2]
    globalPawns = parsedData[3]
    senderId = parsedData[4]

    sio.on("update", handleUpdate)
    sio.on("change_turn", handleTurn)
    sio.on("kill", handleKill)


@sio.event
def handleUpdate(data):
    print('dataUpdate =', data)
    x = data['destination']['x']
    y = data['destination']['y']

    if 'deaths' in data:
        pawn = data['deaths'][- 1]
        killPawn(x, y, pawn)
    else:
        pawn = data['pawn']
        movePawn(x, y, pawn)


@sio.event
def handleTurn(data):
    print('dataTurn =', data)
    if data['senderId'] != data['current']:
        return
    moves = searchMoves()
    kills = searchKills()

    if len(kills) == 0 and len(moves) != 0:
        randomMove(moves)
    elif len(moves) == 0 and len(kills) != 0:
        randomKill(kills)
    else:
        killOrMove = rd.randint(0, 1)
        if killOrMove == 0:
            randomKill(kills)
        else:
            randomMove(moves)


@sio.event
def handleKill(data):
    print('dataKill =', data)


@sio.event
def disconnect():
    print('disconnected from server')


### MAIN ###
sio.connect("http://localhost:3000")
my_message("")

stop = None
while(stop != 'stop'):
    sio.on("start", handleStart)
    # stop = input('type stop to stop: ')


# sio.wait()
sio.disconnect()
