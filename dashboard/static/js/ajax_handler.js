
function ajax_call(command, tx_payload) {

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

            $(".check_mark_image").addClass("shiny_once").show();

            location.reload();

        } else {
            $(".error_mark_image").addClass("shiny_once").show();

        }

    }

}





function activate_busy_mode(){
    $(".disable_while_busy").attr("disabled", true).addClass("disabled");
    $('*').css('cursor','wait')
}



function deactivate_busy_mode(){
    $(".disable_while_busy").removeAttr("disabled").removeClass("disabled");
    $('*').css('cursor','')
}

