const app = require('express')();
var cors = require('cors');
const http = require('http').Server(app);
const io = require('socket.io')(http);

/* var corsOptions = {
    origin: "http://127.0.0.1:8080",
    methods: ["GET", "POST"],
    credentials: true
} */


app.get('/', /* cors(corsOptions),  */(req, res) => {
    res.sendFile(__dirname + '/index.html');
});

io.on('connection', (socket) => {
    console.log('a user connected');

    socket.on('chat message', (msg) => {
        console.log('msg =', msg);
    });

    socket.on('disconnect', () => {
        console.log('user disconnected');
    });
});

http.listen(3001, () => {
    console.log('listening on *:3001');
});