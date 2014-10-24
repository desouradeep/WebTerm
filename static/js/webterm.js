WEB_SOCKET_SWF_LOCATION = "/static/WebSocketMain.swf";
WEB_SOCKET_DEBUG = true;

// Socket.io specific code
var socket = io.connect('/terminal');

// Output/Errors for commands recieved here
socket.on('command', function(payload_string) {
    var payload = JSON.parse(payload_string);
    console.log(payload);
});

// Client UUID sent on this channel on successful connection
socket.on('establish-connection', function(payload_string) {
    var payload = JSON.parse(payload_string);
    webterm_uuid = payload['uuid'];
    console.log("Recieved Client UUID: " + webterm_uuid);
});


$('#start').click(function () {
    var command = $("#command").val();
    var payload = {
        'uuid': webterm_uuid,
        'command': command,
    };
    socket.emit('user message', JSON.stringify(payload));
    return false;
});
