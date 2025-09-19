let candle_chart_data;
var coin = 'ETH';
const verbose = false;

function* range(start, end, step = 1) {
  for (let i = start; i < end; i += step) {
    yield i;
  }
}   

function update_positions_table(payload){

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
            first_cell_html = `<span class="badge rounded-pill bg-primary fs-6">${position.order.name}</span>`

            let stated_cleaned = position.state.replaceAll("_", " ")

            if (position.price < position.stop_loss_price){
                first_cell_html += `<div class="spinner-grow ms-2" style="width: 1px; height: 1px;" role="status">
                                    <span>Exit now</span>
                                </div>`
            }

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
                        <span class="small">(${position.coin_amount})</span>
                        <br>
                        Entry Capital: ${position.order.entry_capital}`

        if (position.stop_loss_price_improved){
            td2_html += `
                            <br>
                            <span style="color: green">profit at increased SLP: ${-position.loss_amount_at_stop_loss_price}</span>
                        `
        }
        else {
            td2_html += `
                            <br>
                            profit at MPEP: ${position.profit_amount_at_profit_take_price}
                        `
            // td2_html += `
            //                 <br>
            //                 profit at MPEP: ${position.profit_amount_at_profit_take_price}
            //                 <br>
            //                 loss at SLP: ${position.loss_amount_at_stop_loss_price}
            //                 <br>
            //                 Ambition Factor: ${position.ambition_ratio}
            //             `
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


        `

        $(`#position_${position.uuid}_td4_html`).html(td4_html);


        const td5_html = `
                        <p>Profit take price: ${position.profit_take_price} </p>

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


    if (payload.alarm){
        $("#alarm_container").html(
            `<div class="alert alert-primary" role="alert">
                ${payload.alarm}
            </div>`
        )
    }


    


    $("#admin_settings_balances_eth").html(         `balance: ${(payload.admin_settings.balances.eth).toFixed(8)} ETH`)
    $("#admin_settings_balances_eth_value").html(   `value: ${(payload.admin_settings.balances.eth * payload.admin_settings.prices.eth).toFixed(2)} USD`)

    $("#admin_settings_balances_weth").html(         `balance: ${(payload.admin_settings.balances.weth).toFixed(8)} WETH`)
    $("#admin_settings_balances_weth_value").html(   `value: ${(payload.admin_settings.balances.weth * payload.admin_settings.prices.eth).toFixed(2)} USD`)

    // $("#admin_settings_balances_wbtc").html(         `${(payload.admin_settings.balances.wbtc).toFixed(8)} WBTC`)
    // $("#admin_settings_balances_wbtc_value").html(   `${(payload.admin_settings.balances.wbtc * payload.admin_settings.prices.btc).toFixed(2)} USD`)


    // $("#admin_settings_balances_wsol").html(         `${(payload.admin_settings.balances.wsol).toFixed(8)} WSOL`)
    // $("#admin_settings_balances_wsol_value").html(   `${(payload.admin_settings.balances.wsol * payload.admin_settings.prices.sol).toFixed(2)} USD`)

    // $("#admin_settings_balances_usdt").html(         `${(payload.admin_settings.balances.usdt).toFixed(2)} USDT`)
    $("#admin_settings_balances_usdc").html(         `balance: ${(payload.admin_settings.balances.usdc).toFixed(2)} USDC`)
    // $("#admin_settings_balances_dai").html(          `${(payload.admin_settings.balances.dai).toFixed(2)} USD`)





    // NEW POSITION CALCULATIONS
    const entry_price            = eval($("#order_entry_price").val());

    const entry_capital_long     = eval($("#entry_capital_long").val());
    const stop_loss_price_long   = eval($("#stop_loss_price_long").val());
    const profit_take_price_long = eval($("#profit_take_price_long").val());

    
    const entry_capital_short     = eval($("#entry_capital_short").val());
    const stop_loss_price_short   = eval($("#stop_loss_price_short").val());
    const profit_take_price_short = eval($("#profit_take_price_short").val());

    if (entry_price > 0) {


        const long_data_present = entry_capital_long && stop_loss_price_long && profit_take_price_long;
        const short_data_present = entry_capital_short && stop_loss_price_short && profit_take_price_short;
        let valid_long_inputs = false;
        let valid_short_inputs = false;

        let long_profit_at_take_profit;
        let long_loss_at_stop_loss;
        let long_ambition_ratio;

        let short_profit_at_take_profit;
        let short_loss_at_stop_loss;
        let short_ambition_ratio;

        if (long_data_present) {
            long_profit_at_take_profit  = entry_capital_long * (profit_take_price_long - entry_price) / entry_price
            long_loss_at_stop_loss      = entry_capital_long * (entry_price - stop_loss_price_long) / entry_price
            long_ambition_ratio         = long_profit_at_take_profit / long_loss_at_stop_loss

            
            $("#long_profit_at_take_profit").html(  `profit at profit take: ${long_profit_at_take_profit.toFixed(2)} (${(100 * long_profit_at_take_profit / entry_capital_long).toFixed(1)} %)`)
            $("#long_loss_at_stop_loss").html(      `loss at stop loss:     ${long_loss_at_stop_loss.toFixed(2)}`)
            $("#long_ambition_ratio").html(         `ambition ratio:        ${long_ambition_ratio.toFixed(2)}`)

            valid_long_inputs = (profit_take_price_long > entry_price) && (entry_price > stop_loss_price_long)
            
            if (valid_long_inputs){
                $("#long_label").removeClass('text-danger')
                $("#long_label").addClass('text-success')
            } else {
                $("#long_label").removeClass('text-success')
                $("#long_label").addClass('text-danger')
                // display_toaster({'message': 'Invalid long inputs', 'color': 'red'})
            }
        } else{
                $("#long_label").removeClass('text-danger')
                $("#long_label").removeClass('text-success')

                $("#long_profit_at_take_profit").html(``)
                $("#long_loss_at_stop_loss").html(``)
                $("#long_ambition_ratio").html(``)

        }



        if (short_data_present) {
            short_profit_at_take_profit  = entry_capital_short * (entry_price - profit_take_price_short) / entry_price
            short_loss_at_stop_loss      = entry_capital_short * (stop_loss_price_short - entry_price) / entry_price
            short_ambition_ratio         = short_profit_at_take_profit / short_loss_at_stop_loss

            
            $("#short_profit_at_take_profit").html(  `profit at profit take: ${short_profit_at_take_profit.toFixed(2)} (${(100 * short_profit_at_take_profit / entry_capital_short).toFixed(1)} %)`)
            $("#short_loss_at_stop_loss").html(      `loss at stop loss:     ${short_loss_at_stop_loss.toFixed(2)}`)
            $("#short_ambition_ratio").html(         `ambition ratio:        ${short_ambition_ratio.toFixed(2)}`)

            
            const safe_borrow_amount = (0.8 * payload.admin_settings.aave_user_account_data.availableBorrowsBase).toFixed(2)

            if (entry_capital_short >= safe_borrow_amount){
                // display_toaster({'message': `you are going to borrow too much. max: ${payload.admin_settings.aave_user_account_data.availableBorrowsBase.toFixed(2)} recommended: ${safe_borrow_amount}`, 'color': 'red'})
            }


            valid_short_inputs = (profit_take_price_short < entry_price) && (entry_price < stop_loss_price_short) //&& (entry_capital_short < safe_borrow_amount)

            
            if (valid_short_inputs){
                $("#short_label").removeClass('text-danger')
                $("#short_label").addClass('text-success')

            } else {
                $("#short_label").removeClass('text-success')
                $("#short_label").addClass('text-danger')

                // display_toaster({'message': 'Invalid short inputs', 'color': 'red'})
            }

        }else{
                $("#short_label").removeClass('text-danger')
                $("#short_label").removeClass('text-success')

                $("#short_profit_at_take_profit").html(``)
                $("#short_loss_at_stop_loss").html(``)
                $("#short_ambition_ratio").html(``)

        }



        if (valid_long_inputs && valid_short_inputs) {

            $("#total_profit_if_price_goes_down").html(`total profit if price goes down: ${(short_profit_at_take_profit - long_loss_at_stop_loss).toFixed(2)}`)
            $("#total_profit_if_price_goes_up").html(`total profit if price goes up: ${(long_profit_at_take_profit - short_loss_at_stop_loss).toFixed(2)}`)

            const start_price = Math.floor(Math.min(stop_loss_price_long, profit_take_price_long, stop_loss_price_short, profit_take_price_short))
            const end_price = Math.floor(Math.max(stop_loss_price_long, profit_take_price_long, stop_loss_price_short, profit_take_price_short))


            let prices = [];
            let long_profits = [];
            let short_profits = [];
            let long_and_short_profits = [];

            for (let price = start_price ; price < end_price ; price += 5) {
                prices.push(price);


                let long_profit = 0;

                if (price < stop_loss_price_long){
                    long_profit = (entry_capital_long * (stop_loss_price_long - entry_price) / entry_price)
                } else if (price > profit_take_price_long) {
                    long_profit = (entry_capital_long * (profit_take_price_long - entry_price) / entry_price)
                }
                else {
                    long_profit = (entry_capital_long * (price - entry_price) / entry_price)
                }

                long_profits.push(long_profit);
                




                let short_profit = 0;

                if (price > stop_loss_price_short){
                    short_profit = (entry_capital_short * (entry_price - stop_loss_price_short) / entry_price)

                } else if (price < profit_take_price_short) {
                    short_profit = (entry_capital_short * (entry_price - profit_take_price_short) / entry_price)

                } else {

                    short_profit = (entry_capital_short * (entry_price - price) / entry_price)
                }
                short_profits.push(short_profit);
                



                

                
                long_and_short_profits.push(short_profit + long_profit);

            }


            

            var trace1 = {
                x: prices,
                y: long_profits,
                name:'Long',
                mode: 'lines',
                type: 'scatter',
                line: {color:'blue'}
                };

            var trace2 = {
                x: prices,
                y: short_profits,
                name:'Short',
                mode: 'lines',
                type: 'scatter',
                line: {color:'red'}

                };

            var trace3 = {
                x: prices,
                y: long_and_short_profits,
                name: "Overall",
                mode: 'lines',
                type: 'scatter',
                line: {color:'green'}

                };

            var data = [trace1, trace2, trace3];

            Plotly.newPlot('new_order_profit_loss_overlook', data);   


        }



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





    // DYNAMIC ELEMENTS
    const most_recent_quote = `

    
                <div class="d-flex justify-content-start gap-5">
                    <div>
                        fiat to coin: ${payload.admin_settings.added_slippage_multiplier_fiat_to_coin} <br>
                        coin to fiat: ${payload.admin_settings.added_slippage_multiplier_coin_to_fiat}
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
    //                     valueAnchor: position.profit_take_price,
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









$(".heart-container").addClass("beat");
    setTimeout(function() {
        $(".heart-container").removeClass("beat");
    }, 1000);



$('#healthFactor').html(`Health factor: ${payload.admin_settings.aave_user_account_data.healthFactor.toFixed(2)}`)
$('#totalDebtBase').html(`Debt: ${payload.admin_settings.aave_user_account_data.totalDebtBase.toFixed(2)} USD`)
$('#totalCollateralBase').html(`Collateral: ${payload.admin_settings.aave_user_account_data.totalCollateralBase.toFixed(2)} USD`)
$('#availableBorrowsBase').html(`Available to borrow: ${payload.admin_settings.aave_user_account_data.availableBorrowsBase.toFixed(2)} USD`)
$('#currentLiquidationThreshold').html(`Liquidation Threshold: ${payload.admin_settings.aave_user_account_data.currentLiquidationThreshold.toFixed(2)}`)


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
    activate_busy_mode();
    console.log(`executing order uuid: ${order_uuid}`);
    ajax_call('execute_order', {'order_uuid': order_uuid})

}



function exit_position(position_uuid){
    activate_busy_mode();
    console.log(`exiting position position uuid: ${position_uuid}`);
    ajax_call('exit_position', {'position_uuid': position_uuid})
}

