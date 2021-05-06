import socketio

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

    print("data =", data)

    boardData = data['board']['data']
    if len(boardData) != 20:
        print('entering if')
        for index in range(0, 20 - len(boardData)):
            boardData.append(None)

    print('boardData =', boardData)
    for index in range(0, len(boardData)):
        if (index in [0, 5, 15, 20]):
            subArray = []
        # print("boardData[index] =", boardData[index])
        # print('index =', index)
        subArray.append(boardData[index])
        if (index in [4, 9, 14, 19]):
            board.append(subArray)

    return width, height, board, pawns, senderId


def searchMoves():
    """returns an array containing the position in the characterRepartition array of all rooms containing only one character"""
    """ movePossibilities = []

    for room, roomIndex in zip(characterRepartition, list(range(0, len(characterRepartition)))):
        if len(room) == 1:
            movePossibilities.append(roomIndex)

    return movePossibilities """

# def dumbMove():
    



### SIO FUNCTIONS ###

@sio.event
def connect():
    print('connection established')


@sio.event
def my_message(data):
    print('message received with ', data)
    sio.emit('room', {'roomName': 'rumble'})


@sio.event
def disconnect():
    print('disconnected from server')


@sio.event
def handleTurn(data):
    print('dataTurn =', data)
    if data['senderId'] != data['current']:
        return
    print('A NOUS')
    pawn = int(input('choose your pawn: '))
    x = int(input('choose your x move: '))
    y = int(input('choose your y move: '))

    


    sio.emit("move", { 'pawn': pawn, 'destination': {'x': x, 'y': y} })

@sio.event
def handleUpdate(data):
    print('dataUpdate =', data)


@sio.event
def handleStart(startData):
    global globalBoard
    global globalPawns
    parsedData = handleData(startData)

    width = parsedData[0]
    height = parsedData[1]
    globalBoard = parsedData[2]
    globalPawns = parsedData[3]
    print('globalBoard =', globalBoard)
    senderId = parsedData[4]

    sio.on("update", handleUpdate)
    sio.on("change_turn", handleTurn)

    

### MAIN ###

sio.connect("http://localhost:3000")
my_message("")

stop = None
while(stop != 'stop'):
    sio.on("start", handleStart)
    # stop = input('type stop to stop: ')


# sio.wait()
sio.disconnect()
