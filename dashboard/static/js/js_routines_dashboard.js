let candle_chart_data;
var coin = 'ETH';
const verbose = false;

function* range(start, end, step = 1) {
  for (let i = start; i < end; i += step) {
    yield i;
  }
}   

function update_positions_table(payload){



    // LIVE CHART
    const anychart_chart_container = document.getElementById("anychart_chart_container");
    if (anychart_chart_container) {
        bot_draw_on_return_anychart(payload);
        populate_indicators_table(payload);
        populate_observation_divs(payload);
    }  
    

    // DEX 
    const dex_tokens_arena__plot = document.getElementById("dex_tokens_arena__plot");
    if (dex_tokens_arena__plot) {
        // dex_draw_token_arena(payload);
        populate_dex_new_tokens_table(payload);
        populate_dex_imported_tokens_table(payload);
    }  
    


    // POSITIONS
    const positions__div = document.getElementById("positions__div");
    if (positions__div) {

        const position_state_color = {
            'in_loss':'danger',
            'reaching_profit_take_price':'success',
            'post_profit_take_price':'success',
            'exited_in_loss':'secondary',
            'exited_in_profit':'secondary',
        }

        payload.positions_dict.forEach(position => {


            let = growth_percentage_from_entry_price_html = ``
            if (position.active){
                    const growth_percentage_from_entry_price_progress_value = position.growth_percentage_from_entry_price > 0 ? 10 * position.growth_percentage_from_entry_price : -10 * position.growth_percentage_from_entry_price
                    const growth_percentage_from_entry_price_progress_color = position.growth_percentage_from_entry_price > 0 ? 'bg-success' : ' bg-danger '
                    growth_percentage_from_entry_price_html = `                        ${position.growth_percentage_from_entry_price} %
                            <div class="progress">
                                <div class="progress-bar ${growth_percentage_from_entry_price_progress_color}" role="progressbar"  style="width: ${growth_percentage_from_entry_price_progress_value}%"  aria-valuenow="${growth_percentage_from_entry_price_progress_value}" aria-valuemin="0" aria-valuemax="100"></div>
                            </div>`
                }




            let first_cell_html = ''
            
            if (position.active){
                first_cell_html = `<span class="badge rounded-pill bg-${position_state_color[position.state]} fs-6">${position.order.name}</span>`

                let stated_cleaned = position.state.replaceAll("_", " ")


                first_cell_html += `
                    <br>
                    <span class="badge rounded-pill bg-${position_state_color[position.state]} m-1">
                        ${stated_cleaned}
                    </span>
                `

                if (position.stop_loss_price_improved){
                    first_cell_html += `
                        <i class="bi bi-check m-0 elementToFade"  style="font-size: 3rem; color: aquamarine;"></i>
                    `
    
                }

            } else {
                first_cell_html = `<span class="badge rounded-pill bg-secondary">${position.order.name}</span>`
            }



            $(`#position_${position.uuid}_first_cell_html`).html(first_cell_html);



            let td2_html = `
                                ${position.order.coin}
                                <br>
                                Entry Capital: ${position.order.entry_capital}
                            `

                            if (position.is_long){
                                td2_html += `
                                <br>
                                <span class="small">(${position.coin_amount_long})</span>
                                <br>`
                            }


                td2_html += `
                                <br>
                                profit at PT: ${position.profit_amount_at_profit_take_price}
                            `
                // td2_html += `
                //                 <br>
                //                 profit at MPEP: ${position.profit_amount_at_profit_take_price}
                //                 <br>
                //                 loss at SLP: ${position.loss_amount_at_stop_loss_price}
                //                 <br>
                //                 Ambition Factor: ${position.ambition_ratio}
                //             `

            $(`#position_${position.uuid}_td2_html`).html(td2_html);



            const td3_html = `
                            Entry price: ${position.entry_price} <br>
                            <p>price: <strong>${position.price}</strong></p>

                            ${growth_percentage_from_entry_price_html}
            `

            $(`#position_${position.uuid}_td3_html`).html(td3_html);



            const td4_html = `
                            Stop loss: ${position.stop_loss_price} <br>
                            Initial stop loss: ${position.initial_stop_loss_price} <br>


            `

            $(`#position_${position.uuid}_td4_html`).html(td4_html);


            const td5_html = `
                            <p>Stop loss: ${position.stop_loss_price} </p>
                            <p>Profit take: ${position.profit_take_price} </p>

            `

            $(`#position_${position.uuid}_td5_html`).html(td5_html);



            let td6_html = `
                        Value: $ ${position.value}<br>
                        Growth: $ 

            `

            if (position.growth_usd > 0){
                td6_html += `<span class="badge rounded-pill bg-success fs-6">${position.growth_usd}</span>`
            } else {
                td6_html += `<span class="badge rounded-pill bg-danger fs-6">${position.growth_usd}</span>`
            }

            $(`#position_${position.uuid}_td6_html`).html(td6_html);



        });

    }  






    // ORDERS & PAIRS
    if (window.location.pathname.includes('orders/') || window.location.pathname.includes('pair/')){


            let entry_price_long;
            let entry_price_short;

            let entry_capital_long;
            let stop_loss_price_long;
            let profit_take_price_long;

            
            let entry_capital_short;
            let stop_loss_price_short;
            let profit_take_price_short;
        


            // if (window.location.pathname.includes('orders/')){
            
                // entry_price_long       = eval($("#order_entry_price").val());
                // entry_price_short      = eval($("#order_entry_price").val());
            
            // } else if (window.location.pathname.includes('pair/')){

                entry_price_long       = eval($("#entry_price_long").val());
                entry_price_short      = eval($("#entry_price_short").val());
            // }


                entry_capital_long     = eval($("#entry_capital_long").val());
                stop_loss_price_long   = eval($("#stop_loss_price_long").val());
                profit_take_price_long = eval($("#profit_take_price_long").val());

                
                entry_capital_short     = eval($("#entry_capital_short").val());
                stop_loss_price_short   = eval($("#stop_loss_price_short").val());
                profit_take_price_short = eval($("#profit_take_price_short").val());


        if ((entry_price_long > 0) && (entry_price_short > 0)) {




            draw_pairs_plot(
                payload.admin_settings.prices.weth,
                entry_price_long,
                entry_price_short,

                entry_capital_long,
                stop_loss_price_long,
                profit_take_price_long,
                entry_capital_short,
                stop_loss_price_short,
                profit_take_price_short,        

            );

        }
        
    }

    
    




    
    // BASE ELEMENTS


    if (payload.alarm){
        $("#alarm_container").html(
            `<div class="alert alert-primary" role="alert">
                ${payload.alarm}
            </div>`
        )
    }


    


    $("#admin_settings_balances_eth").html(         `balance: ${(payload.admin_settings.balances.eth).toFixed(8)} ETH`)
    $("#admin_settings_balances_eth_value").html(   `value: ${(payload.admin_settings.balances.eth * payload.admin_settings.prices.weth).toFixed(2)} USD`)

    $("#admin_settings_balances_weth").html(         `balance: ${(payload.admin_settings.balances.weth).toFixed(8)} WETH`)
    $("#admin_settings_balances_weth_value").html(   `value: ${(payload.admin_settings.balances.weth * payload.admin_settings.prices.weth).toFixed(2)} USD`)

    // $("#admin_settings_balances_wbtc").html(         `${(payload.admin_settings.balances.wbtc).toFixed(8)} WBTC`)
    // $("#admin_settings_balances_wbtc_value").html(   `${(payload.admin_settings.balances.wbtc * payload.admin_settings.prices.btc).toFixed(2)} USD`)


    // $("#admin_settings_balances_wsol").html(         `${(payload.admin_settings.balances.wsol).toFixed(8)} WSOL`)
    // $("#admin_settings_balances_wsol_value").html(   `${(payload.admin_settings.balances.wsol * payload.admin_settings.prices.sol).toFixed(2)} USD`)

    // $("#admin_settings_balances_usdt").html(         `${(payload.admin_settings.balances.usdt).toFixed(2)} USDT`)
    $("#admin_settings_balances_usdc").html(         `balance: ${(payload.admin_settings.balances.usdc).toFixed(2)} USDC`)
    // $("#admin_settings_balances_dai").html(          `${(payload.admin_settings.balances.dai).toFixed(2)} USD`)



    var delta_time_gas_update_html = ''
    var delta_time_price_update_html = ''
    var valid_beat_data = false;

    try {

        if (payload.admin_settings.gas.gas_basic_price > payload.admin_settings.max_sane_gas_price){
            $("#gas_price").html(`<span class=" rounded p-1 bg-danger elementToFade">GAS: ${payload.admin_settings.gas.gas_basic_price}</span> > ${payload.admin_settings.max_sane_gas_price}`);
            $(".gas_sensetive_dom").prop("disabled",true);
        }
        else{
            $("#gas_price").html(`GAS: ${payload.admin_settings.gas.gas_basic_price}`);
            $(".gas_sensetive_dom").prop("disabled",false);

        }


        $("#weth_price").html(`weth price: ${payload.admin_settings.prices.weth}`);
        // $("#wbtc_price").html(`wbtc: ${payload.admin_settings.prices.wbtc}`);
        // $("#wsol_price").html(`wsol: ${payload.admin_settings.prices.wsol}`);

        const epochSeconds = Math.floor(Date.now() / 1000);   
        const delta_time_price_update = epochSeconds - payload.admin_settings.prices_update_epoch;
        const delta_time_gas_update = epochSeconds - payload.admin_settings.gas_update_epoch;

        


        if (delta_time_price_update < 5) {
            delta_time_price_update_html = `<p >price updated: ${delta_time_price_update}</p>`
        } else {
            delta_time_price_update_html = `<p class="bg-danger elementToFade rounded p-1">price updated: ${delta_time_price_update}</p>`
        }

        if (delta_time_gas_update < payload.admin_settings.gas_update_epoch_max_allowed_delay_seconds) {
            delta_time_gas_update_html = `<p >gas updated: ${delta_time_gas_update}</p>`
        } else {
            delta_time_gas_update_html = `<p class="bg-danger elementToFade rounded p-1">gas updated: ${delta_time_gas_update}</p>`
        }
        valid_beat_data = true;

    } catch{

        delta_time_gas_update_html = `<p class="bg-danger elementToFade rounded p-1">gas updated: ERROR</p>`
        delta_time_price_update_html = `<p class="bg-danger elementToFade rounded p-1">price updated: ERROR</p>`
    }


    $("#prices_update_epoch").html(delta_time_price_update_html);
    $("#gas_update_epoch").html(delta_time_gas_update_html);






    const most_recent_quote = `

    
                <div class="d-flex justify-content-start gap-5">
                    <div>
                        fiat to coin: ${payload.admin_settings.uniswap_asm_fiat_to_token} <br>
                        coin to fiat: ${payload.admin_settings.uniswap_asm_token_to_fiat}
                    </div>
                </div>


        
    
    `
    $("#most_recent_quote").html(most_recent_quote);







    $(".heart-container").addClass("beat");
        setTimeout(function() {
            $(".heart-container").removeClass("beat");
        }, 1000);


    try{
    $('#healthFactor').html(`Health factor: ${payload.admin_settings.aave_user_account_data.healthFactor.toFixed(2)}`)
    $('#totalDebtBase').html(`Debt: ${payload.admin_settings.aave_user_account_data.totalDebtBase.toFixed(2)} USD`)
    $('#totalCollateralBase').html(`Collateral: ${payload.admin_settings.aave_user_account_data.totalCollateralBase.toFixed(2)} USD`)
    $('#availableBorrowsBase').html(`Available to borrow: ${payload.admin_settings.aave_user_account_data.availableBorrowsBase.toFixed(2)} USD`)
    $('#currentLiquidationThreshold').html(`Liquidation Threshold: ${payload.admin_settings.aave_user_account_data.currentLiquidationThreshold.toFixed(2)}`)
    } catch{}

}



function logger_to_frontend(payload){
    console.log(payload);
    const textarea = document.getElementById('logger_textarea');
    textarea.value = `${payload}\n${textarea.value}`;   

}

function refresh_page(){
    location.reload();
}

function display_toaster(payload){
    Toastify({

        text: payload.message,
        style: {
            background: payload.color,
        },
        duration: 3000

    }).showToast();
}


function update_balances(){
    ajax_call('update_balances', {})
}

function update_both_way_quotes(){
    const fiat_amount_in = eval($("#entry_capital").val());
    if (fiat_amount_in > 0){
        ajax_call('update_both_way_quotes', {'fiat_amount_in': fiat_amount_in});
    }

}



function display_position_on_chart(position_uuid){
    ajax_call('display_position_on_chart', {'position_uuid': position_uuid})
}




function execute_order(order_uuid){

    ajax_call('execute_order', {'order_uuid': order_uuid})

}



function exit_position(position_uuid){

    
    ajax_call('exit_position', {'position_uuid': position_uuid})
}

