

function setup_ws(){

    let protocol;

    if (window.location.host === "127.0.0.1:8000") {
        protocol = 'ws';
    } else {
        protocol = 'wss'
    }

    const conn_string = protocol + '://'+ window.location.host+ '/ws/dashboard/'+ '1'+ '/';

    const socket = new WebSocket(conn_string);

    socket.onmessage = function (message_event) {
        ws_msg_handler(message_event)
    };

    if (verbose) {
        console.info(`ws service activated on ${conn_string}`);
    }

}