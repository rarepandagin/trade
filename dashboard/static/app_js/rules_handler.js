

function populate_rules_view(){

    $('#rules__div').html(generate_rules_view_html());

    reflect_rules_to_ui();

}



function generate_rules_view_html(){


    var rooms_html = ``

    const rooms = Object.keys(user_profile_object.rules);
    for (let room of rooms) {

        const value = user_profile_object.rules[room];

        if(value.show){

            rooms_html += `
                        <tr >
                            <td>
                                
                                <p class="fw-bolder text-primary ">${make_titled(room)}</p>
                    
                            </td>
                            
                            <td>
                    
                                <input type="number" min="3" max="20" id="rule_${room}_dim_min__input" class="form-control form-control-sm disable_while_busy" >
                    
                            </td>
                                    
                            <td>
                    
                                <input type="number" min="40" max="400" id="rule_${room}_area_min__input" class="form-control form-control-sm disable_while_busy" >
                    
                            </td>
                                
                            <td>
                    
                                <input type="number" min="1.0" max="2.0" step="0.1" id="rule_${room}_aspect_ratio__input" class="form-control form-control-sm disable_while_busy" >
                    
                            </td>
                            
                            
                            <td>
                            
                                <div class="form-check">
                                  <input class="form-check-input disable_while_busy" type="checkbox" id="rule_${room}_window__check">
                                </div>
                    
                            </td>
            
            
                        </tr>`

        }
    }




    var html = `



    <br>
    
    <table class="table-bordered table-sm text-secondary-emphasis rounded" style="width: 90%;">
    
        <colgroup>
            <col span="1" style="width: 10%;">
            <col span="1" style="width: 25%;">
            <col span="1" style="width: 25%;">
            <col span="1" style="width: 25%;">
            <col span="1" style="width: 15%;">
        </colgroup>

        <thead>
            
                <tr>
                    <td></td>
                    <td><p class="fw-normal text-primary  mb-0">Min dimension</p></td>
                    <td><p class="fw-normal text-primary  mb-0">Min area</p></td>
                    <td><p class="fw-normal text-primary  mb-0">Aspect ratio</p></td>
                    <td><p class="fw-normal text-primary  mb-0">Has windows</p></td>
                </tr>
                
        </thead>

        <tbody>
            
            ${rooms_html}
    
        </tbody>

    </table>
    

    
    
    `




    return html

}


// rules --> UI
function reflect_rules_to_ui(){

    const rooms = Object.keys(user_profile_object.rules);

    for (let room of rooms) {

        const value = user_profile_object.rules[room];

            if(value.show) {

                $(`#rule_${room}_dim_min__input`).val(`${user_profile_object.rules[room].dim_min}`)
                $(`#rule_${room}_area_min__input`).val(`${user_profile_object.rules[room].area_min}`)
                $(`#rule_${room}_aspect_ratio__input`).val(`${user_profile_object.rules[room].aspect_ratio}`)
                $(`#rule_${room}_window__check`).prop('checked', user_profile_object.rules[room].window)
            }
    }

}


// UI --> rules
function update_rules_per_ui(){



    const rooms = Object.keys(user_profile_object.rules);

    for (let room of rooms) {

        const value = user_profile_object.rules[room];

            if(value.show) {

                user_profile_object.rules[room].dim_min = parseInt($(`#rule_${room}_dim_min__input`).val());
                user_profile_object.rules[room].area_min = parseInt($(`#rule_${room}_area_min__input`).val());
                user_profile_object.rules[room].aspect_ratio = parseFloat($(`#rule_${room}_aspect_ratio__input`).val());
                user_profile_object.rules[room].window = ($(`#rule_${room}_window__check`).prop('checked')) ? 1: 0;

            }
    }

    ajax_call('save_rules',{'room_rules': user_profile_object.rules})

}

