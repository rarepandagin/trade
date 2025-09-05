


function update_positions_table(payload){


    let rows = ``


    const position_state_color = {
        'in_loss':'danger',
        'reaching_min_profit_exit_price':'success',
        'post_min_profit_exit_price':'success',
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

        let growth_percentage_from_stop_loss_price_html = ``

        // if (position.active){

        //     const growth_percentage_from_stop_loss_price_progress_value = position.growth_percentage_from_stop_loss_price > 0 ? position.growth_percentage_from_stop_loss_price : - position.growth_percentage_from_stop_loss_price
        //     const growth_percentage_from_stop_loss_price_progress_color = position.growth_percentage_from_stop_loss_price > 0 ? 'bg-success' : ' bg-danger '
        //     growth_percentage_from_stop_loss_price_html = `
        //                 <p class="small">progress from stop loss to profit: ${position.growth_percentage_from_stop_loss_price} %</p>
        //                 <div class="progress">
        //                     <div class="progress-bar ${growth_percentage_from_stop_loss_price_progress_color}" role="progressbar"  style="width: ${growth_percentage_from_stop_loss_price_progress_value}%"  aria-valuenow="${growth_percentage_from_stop_loss_price_progress_value}" aria-valuemin="0" aria-valuemax="100"></div>
        //                 </div>
        //     `
        // }

        let growth_percentage_from_min_profit_exit_price = ``
        // if (position.active){

        //     const growth_percentage_from_min_profit_exit_price_progress_value = position.growth_percentage_from_min_profit_exit_price > 0 ? position.growth_percentage_from_min_profit_exit_price : -position.growth_percentage_from_min_profit_exit_price
        //     const growth_percentage_from_min_profit_exit_price_progress_color = position.growth_percentage_from_min_profit_exit_price > 0 ? 'bg-success' : ' bg-danger '
        //     growth_percentage_from_min_profit_exit_price = `                        <p class="small">progress from entry to profit: ${position.growth_percentage_from_min_profit_exit_price} %</p>
        //                 <div class="progress">
        //                     <div class="progress-bar ${growth_percentage_from_min_profit_exit_price_progress_color}" role="progressbar"  style="width: ${growth_percentage_from_min_profit_exit_price_progress_value}%"  aria-valuenow="${growth_percentage_from_min_profit_exit_price_progress_value}" aria-valuemin="0" aria-valuemax="100"></div>
        //                 </div>`
        // }

        let first_cell_html = ''
        
        if (position.active){
            first_cell_html = `<span class="badge rounded-pill bg-primary fs-6">${position.order.name}</span>`

                
            if (position.price < position.stop_loss_price){
                first_cell_html += `<div class="spinner-grow ms-2" style="width: 1px; height: 1px;" role="status">
                                    <span>Exit now</span>
                                </div>`
            }
            first_cell_html += `
                <br>
                <span class="badge rounded-pill bg-${position_state_color[position.state]}">
                    ${position.state}
                </span>
            `

            if (position.stop_loss_price_increased){
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
                        (${position.coin_amount})
                        <br>
                        Entry Capital: ${position.order.entry_capital}`

        if (position.stop_loss_price_increased){
            td2_html += `
                            <br>
                            <span style="color: green">profit at increased SLP: ${-position.loss_amount_at_stop_loss_price}</span>
                        `
        }
        else {
            td2_html += `
                            <br>
                            profit at MPEP: ${position.profit_amount_at_min_profit_exit_price}
                            <br>
                            loss at SLP: ${position.loss_amount_at_stop_loss_price}
                            <br>
                            Ambition Factor: ${position.ambition_ratio}
                        `
        }

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

                        ${growth_percentage_from_stop_loss_price_html}

        `

        $(`#position_${position.uuid}_td4_html`).html(td4_html);


        const td5_html = `
                        <p>Min profit exit price: ${position.min_profit_exit_price} </p>

                        ${growth_percentage_from_min_profit_exit_price}


        `

        $(`#position_${position.uuid}_td5_html`).html(td5_html);



        const td6_html = `
                    Value: $ ${position.value}<br>
                    Growth: $ ${position.growth_usd}

        `

        $(`#position_${position.uuid}_td6_html`).html(td6_html);



    });


    if (payload.alarm){
        $("#alarm_container").html(
            `<div class="alert alert-primary" role="alert">
                ${payload.alarm}
            </div>`
        )
    }


    


    $("#admin_settings_balances_eth").html(         `${(payload.admin_settings.balances.eth).toFixed(8)} ETH`)
    $("#admin_settings_balances_eth_value").html(   `${(payload.admin_settings.balances.eth * payload.admin_settings.prices.eth).toFixed(2)} USD`)

    $("#admin_settings_balances_weth").html(         `${(payload.admin_settings.balances.weth).toFixed(8)} WETH`)
    $("#admin_settings_balances_weth_value").html(   `${(payload.admin_settings.balances.weth * payload.admin_settings.prices.eth).toFixed(2)} USD`)

    $("#admin_settings_balances_wbtc").html(         `${(payload.admin_settings.balances.wbtc).toFixed(8)} WBTC`)
    $("#admin_settings_balances_wbtc_value").html(   `${(payload.admin_settings.balances.wbtc * payload.admin_settings.prices.btc).toFixed(2)} USD`)


    $("#admin_settings_balances_wsol").html(         `${(payload.admin_settings.balances.wsol).toFixed(8)} WSOL`)
    $("#admin_settings_balances_wsol_value").html(   `${(payload.admin_settings.balances.wsol * payload.admin_settings.prices.sol).toFixed(2)} USD`)

    $("#admin_settings_balances_usdt").html(         `${(payload.admin_settings.balances.usdt).toFixed(2)} USDT`)
    $("#admin_settings_balances_usdc").html(         `${(payload.admin_settings.balances.usdc).toFixed(2)} USDC`)
    $("#admin_settings_balances_dai").html(          `${(payload.admin_settings.balances.dai).toFixed(2)} USD`)





    // NEW POSITION CALCULATIONS

    const entry_capital_input_value = eval($("#entry_capital").val());
    const stop_loss_price_input_value = eval($("#stop_loss_price").val());
    const min_profit_exit_price = eval($("#min_profit_exit_price").val());

    var new_position_coin_price = payload.admin_settings.prices[$("#new_position_coin_select").val()]

    if (entry_capital_input_value && stop_loss_price_input_value && min_profit_exit_price){

        let profit_amount_at_min_profit_exit_price = (min_profit_exit_price - new_position_coin_price) * (entry_capital_input_value / new_position_coin_price);
        let loss_amount_at_stop_loss_price = (new_position_coin_price - stop_loss_price_input_value) * (entry_capital_input_value / new_position_coin_price);
        let ambition_ratio = profit_amount_at_min_profit_exit_price / loss_amount_at_stop_loss_price;
        

        $("#profit_amount_at_min_profit_exit_price").html(`profit_amount_at_min_profit_exit_price: ${profit_amount_at_min_profit_exit_price.toFixed(2)}`)
        $("#loss_amount_at_stop_loss_price").html(`loss_amount_at_stop_loss_price: ${loss_amount_at_stop_loss_price.toFixed(2)}`)
        $("#ambition_ratio").html(`ambition_ratio: ${ambition_ratio.toFixed(2)}`)
    }
    



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


        $("#weth_price").html(`weth: ${payload.admin_settings.prices.weth}`);
        $("#wbtc_price").html(`wbtc: ${payload.admin_settings.prices.wbtc}`);
        $("#wsol_price").html(`wsol: ${payload.admin_settings.prices.wsol}`);

        const epochSeconds = Math.floor(Date.now() / 1000);   
        const delta_time_price_update = epochSeconds - payload.admin_settings.prices_update_epoch;
        const delta_time_gas_update = epochSeconds - payload.admin_settings.gas_update_epoch;

        


        if (delta_time_price_update < 5) {
            delta_time_price_update_html = `<p >price updated: ${delta_time_price_update}</p>`
        } else {
            delta_time_price_update_html = `<p class="bg-danger elementToFade rounded p-1">price updated: ${delta_time_price_update}</p>`
        }

        if (delta_time_gas_update < 5) {
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





    // DYNAMIC ELEMENTS
    const most_recent_quote = `

    
                <div class="d-flex justify-content-start gap-5">
                    <div>
                        fiat to coin: ${payload.admin_settings.added_slipage_multiplier_fiat_to_coin} <br>
                        coin to fiat: ${payload.admin_settings.added_slipage_multiplier_coin_to_fiat}
                    </div>
                </div>


        
    
    `
    $("#most_recent_quote").html(most_recent_quote);


    // $("#chart_container").html("")

    // anychart.format.outputTimezone(-240);

    // candle_chart_data = "'Date,Open,High,Low,Close,y,x"

    // payload.candles_dict.forEach(x=>{
    //     candle_chart_data += `\n${x.open_time},${x.open},${x.high},${x.low},${x.close},${x.volume},${x.ema}`
    // })
    // candle_chart_data += "'"

    //   // create a data table with the loaded data
    //   var dataTable = anychart.data.table();

    //   dataTable.addData(candle_chart_data);
    //   // map the loaded data for the candlestick series
    //   var mapping_candlestick = dataTable.mapAs({
    //     open: 1,
    //     high: 2,
    //     low: 3,
    //     close: 4
    //   });
    //   // create a stock chart
    //   var chart = anychart.stock();
    //   // create the chart plot
    //   var plot = chart.plot(0);


    //   // Annotations
    //   var controller = plot.annotations();

    //     payload.positions_dict.forEach(position => {
    //         if (position.coin === coin){
    //             if (position.display_on_chart){
    //             if (position.active){
                    
    //                 controller.horizontalLine({
    //                     valueAnchor: position.entry_price,
    //                     stroke: "1 #0011ffff"
    //                 });

    //                 controller.horizontalLine({
    //                     valueAnchor: position.stop_loss_price,
    //                     stroke: "1 #ff0000ff"
    //                 });
    //                 controller.horizontalLine({
    //                     valueAnchor: position.min_profit_exit_price,
    //                     stroke: "1 #48ff00ff"
    //                 });


    //             }
    //             }
    //         }
    //     })



    //   // set the grid settings
    //   plot
    //     .yGrid(true)
    //     .xGrid(true)
    //     .yMinorGrid(true)
    //     .xMinorGrid(true);

    //   // create the candlestick series
    //   var series_candlestick = plot.candlestick(mapping_candlestick);
    //   series_candlestick.name('TSMC');
    //   series_candlestick.legendItem().iconType('rising-falling');
      
	// // map the data for all series
	// var mapping_ema = dataTable.mapAs({x: 0, value: 6});
	// var firstSeries = plot.line(mapping_ema);
    //   firstSeries.name('EMA');
    //   firstSeries.legendItem().iconType('DDD-falling');


	// // var mapping_ema = dataSet.mapAs({x: 0, value: 1})
	// //   var series_ema = chart.plot(0).line(mapping_ema);


    //     // const yScale = anychart.scales.linear().minimum(110000).maximum(120000);
    //     // plot.yScale(yScale);   
    //   // set the title of the chart
    //   chart.title('TSMC Stock Chart');
    //   // set the container id for the chart
    //   chart.container('chart_container');
    //   // initiate the chart drawing
    //   chart.draw();











    
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