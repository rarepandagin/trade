
function ajax_call(command, tx_payload) {
    
    activate_busy_mode()

    $.ajax({
        type: "POST",
        url: "",
        data: {
            'payload': JSON.stringify(tx_payload),
            'req': command,
        },
        headers: {
            "X-CSRFToken": "{{ csrf_token }}",

        },
        success: function (ret_val) {

            handle_ajax_returns(ret_val);

        }
    })
}





function handle_ajax_returns(ret){

    deactivate_busy_mode();


    if (ret?.req){
        

        if (ret.success){

            if (ret.req == 'bot_draw_data')
            {
                bot_draw_data_on_return(ret.returned_payload)
            }
            // location.reload();

        } else {

        }

    }

}





function activate_busy_mode(){
    $(".disable_while_busy").attr("disabled", true).addClass("disabled");
    $(".btn").attr("disabled", true).addClass("disabled");
    $('*').css('cursor','wait')
}



function deactivate_busy_mode(){
    $(".disable_while_busy").removeAttr("disabled").removeClass("disabled");
    $(".btn").removeAttr("disabled").removeClass("disabled");
    $('*').css('cursor','')
}

