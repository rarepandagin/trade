

function populate_inputs_view(){

    $('#inputs__div').html(generate_inputs_view_html());

    reflect_inputs_to_ui();

}



function generate_inputs_view_html(){


    var floors_html = ``

    for (let i = 0; i < user_profile_object.inputs.floors_count; i++) {

        floors_html += `
                    <tr >
                        <td>
                            
                            <p class="small m-1">${i+1}</p>
                
                        </td>
                        
                        <td>
                
                            <input type="number" min="0" max="3" value="1" id="floor_${i}_bedroom__input" class="form-control form-control-sm disable_while_busy" >
                
                        </td>
                                
                        <td>
                
                            <input type="number" min="0" max="3" value="1" id="floor_${i}_master_bedroom__input" class="form-control form-control-sm disable_while_busy" >
                
                        </td>
                            
                        <td>
                
                            <input type="number" min="0" max="3" value="1" id="floor_${i}_bath__input" class="form-control form-control-sm disable_while_busy" >
                
                        </td>
                        
                        
                        
        
                    </tr>`

    }


    var html = `


    <div class="hstack gap-3 mt-2">
    <p class="fw-normal mt-3">Floors count:</p>
    <select class="form-select form-select-sm disable_while_busy" id="floors_count__select" aria-label="Default select example" style="width: 100px" onchange="update_inputs_per_ui();populate_inputs_view();">
      <option value="1">One</option>
      <option value="2">Two</option>
      <option value="3">Three</option>

    </select>
    </div>
    
    <br>    
    <table class="table-bordered table-sm w-100 rounded bg-white">
    
                <colgroup>
                    <col span="1" style="width: 10%;">
                    <col span="1" style="width: 30%;">
                    <col span="1" style="width: 30%;">
                    <col span="1" style="width: 30%;">
                </colgroup>
    
                <thead>
                    
                        <tr>
                            <td><h6 class="m-0 fw-normal text-primary">Floor</h6></td>
                            <td><h6 class="m-0 fw-normal text-primary">Bedrooms</h6></td>
                            <td><h6 class="m-0 fw-normal text-primary">Master Bedrooms</h6></td>
                            <td><h6 class="m-0 fw-normal text-primary">Bathrooms</h6></td>
                        </tr>
                        
                </thead>
    
                <tbody>
                    
                    ${floors_html}
            
            

                </tbody>
    
                </table>
                
                
                <table class="table-sm  mt-5 rounded w-100 bg-white">
                    <tr>
                        <td><p class="fw-normal ">Include a garage</p></td>
                        <td>
                            <div class="form-check">
                              <input class="form-check-input disable_while_busy" type="checkbox"  id="has_garage__check">
                            </div>
                        </td>
                    </tr>
                    <tr>
                        <td><p class="fw-normal">Horizontal length (ft):</p></td>
                        <td>
                            <div class="hstack ">
                            <input type="number" min="10" max="300" class="form-control form-control-sm disable_while_busy" id="tmr_settings_width__input" style="width: 100%"/>
                        </td>
                    </tr>
                    <tr>
                        <td><p class="fw-normal">Vertical length (ft):</p></td>
                        <td>
                            <div class="hstack ">
                            <input type="number" min="10" max="300" class="form-control form-control-sm disable_while_busy" id="tmr_settings_height__input" style="width: 100%"/>
                        </td>
                    </tr>
                </table>
                
                
                
                
    
    `




    return html

}


// inputs --> UI
function reflect_inputs_to_ui(){

    $("#floors_count__select").val(user_profile_object.inputs.floors_count)
    $("#tmr_settings_width__input").val(user_profile_object.inputs.width)
    $("#tmr_settings_height__input").val(user_profile_object.inputs.height)

    $(`#has_garage__check`).prop('checked', user_profile_object.inputs.levels[0].garage)


    for (let i = 0; i < user_profile_object.inputs.floors_count; i++) {

        $(`#floor_${i}_bedroom__input`).val(`${user_profile_object.inputs.levels[i].bedroom}`)
        $(`#floor_${i}_master_bedroom__input`).val(`${user_profile_object.inputs.levels[i].master_bedroom}`)
        $(`#floor_${i}_bath__input`).val(`${user_profile_object.inputs.levels[i].bath}`)

    }





}


// UI --> inputs
function update_inputs_per_ui(){

    user_profile_object.inputs.floors_count = parseInt($("#floors_count__select").val());
    user_profile_object.inputs.width = parseInt($("#tmr_settings_width__input").val());
    user_profile_object.inputs.height = parseInt($("#tmr_settings_height__input").val());

    user_profile_object.inputs.levels = []

    for (let i = 0; i < user_profile_object.inputs.floors_count; i++) {

        let bedroom = parseInt($(`#floor_${i}_bedroom__input`).val())
        let master_bedroom = parseInt($(`#floor_${i}_master_bedroom__input`).val())
        let bath = parseInt($(`#floor_${i}_bath__input`).val())

        user_profile_object.inputs.levels.push({
            "bedroom": (bedroom !== undefined)? bedroom: 1,
            "master_bedroom": (master_bedroom !== undefined)? master_bedroom: 0,
            "bath":  (bath !== undefined)? bath: 0,
            "kitchen": 0,
            "garage":  0,
        })

    }

    user_profile_object.inputs.levels[0].garage = ($(`#has_garage__check`).prop('checked'))? 1 : 0

}