import socketio
sio = socketio.Client()


### AI FUNCTIONS ###

def handleData(data):
    width = data['board']['width']
    height = data['board']['height']
    board = []
    pawns = data['pawns']
    senderId = data['senderId']

    boardData = data['board']['data']
    for index in range(len(boardData) - 1, 0, -1):
        if (index in [19, 14, 9, 4]):
            subArray = []
        subArray.append(boardData[index])
        if (index in [19, 14, 9, 4]):
            board.append(subArray)

    return width, height, board, pawns, senderId


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
def handleStart(startData):
    parsedData = handleData(startData)

    width = parsedData[0]
    height = parsedData[1]
    board = parsedData[2]
    pawns = parsedData[3]
    senderId = parsedData[4]

    print('width =', width)
    print('height =', height)
    print('board =', board)
    print('pawns =', pawns)
    print('senderId =', senderId)


### MAIN ###

sio.connect("http://localhost:3000")
my_message("")

while True:
    sio.on("start", handleStart)
    input()

# sio.wait()
# sio.disconnect()
