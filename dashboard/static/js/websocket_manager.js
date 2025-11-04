

function setup_ws_dashboard(){

    let protocol;

    if (window.location.host === "127.0.0.1:8000") {
        protocol = 'ws';
    } else {
        protocol = 'wss'
    }

    const conn_string = `${protocol}://${window.location.host}/ws/dashboard/`;

    const socket = new WebSocket(conn_string);

    socket.onmessage = function (message_event) {
        ws_msg_handler_dashboard(message_event)
    };

    console.info(`v11 ws service activated on ${conn_string}`);

}

function setup_ws_depth(){

    let protocol;

    if (window.location.host === "127.0.0.1:8000") {
        protocol = 'ws';
    } else {
        protocol = 'wss'
    }

    const conn_string = `${protocol}://${window.location.host}/ws/depth/`;

    const socket = new WebSocket(conn_string);

    socket.onmessage = function (message_event) {
        ws_msg_handler_depth(message_event)
    };

    console.info(`v11 ws service activated on ${conn_string}`);

}


function ws_msg_handler_dashboard(message_event) {


    // if (!window.location.pathname.includes('/dashboard/')) {
    //     return;
    // }

    let incoming_message;

    try {
        incoming_message = JSON.parse(message_event.data).message;
        console.log('.');
        


    } catch (error) {
        deactivate_busy_mode()
        console.error(error)
        return;
    }

    

    incoming_message.payload.admin_settings = JSON.parse(incoming_message.payload.admin_settings)

    

    if (incoming_message.topic === "update_positions_table"){

        update_positions_table(incoming_message.payload)

    } else if (incoming_message.topic === "refresh_page"){

        refresh_page();

    } else if (incoming_message.topic === "logger_to_frontend"){
        
        logger_to_frontend(incoming_message.payload)
    
    } else if (incoming_message.topic === "display_toaster"){
        
        display_toaster(incoming_message.payload)
    
    }

}




function ws_msg_handler_depth(message_event) {

    // if (!window.location.pathname.includes('/depth/')) {
    //     return;
    // }

    let incoming_message;

    try {
        incoming_message = JSON.parse(message_event.data).message;
        console.log(',');
        
    } catch (error) {
        console.error(error)
        return;
    }

    if (incoming_message.topic === "update_depth_chart"){
        update_depth_chart(incoming_message.payload);
    }


    
}