
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


            if (ret_val?.req){

                if (ret_val.success){

                    if (ret_val.req === 'save_rules') {

                        window.location.href = `/dashboard/`;

                    }

                }

            }

        }
    })
}



function activate_busy_mode(){
    $(".disable_while_busy").attr("disabled", true).addClass("disabled");
    $('*').css('cursor','wait')
}



function deactivate_busy_mode(){
    $(".disable_while_busy").removeAttr("disabled").removeClass("disabled");
    $('*').css('cursor','')
}
