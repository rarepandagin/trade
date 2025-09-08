

function ws_msg_handler(message_event) {


    if (!window.location.pathname.includes('/dashboard/')) {
        return;
    }

    let incoming_message;

    try {
        incoming_message = JSON.parse(message_event.data).message;
        console.log(incoming_message);
        

    } catch (error) {
        deactivate_busy_mode()
        console.error(error)
        return;
    }

    



    

    if (incoming_message.topic === "update_positions_table"){

        update_positions_table(incoming_message.payload)


    }

}

