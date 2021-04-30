import socketio

sio = socketio.Client()


sio.connect('http://localhost:3001')
sio.emit('chat message', 'test')
# sio.wait()
sio.sleep(2)
sio.disconnect()