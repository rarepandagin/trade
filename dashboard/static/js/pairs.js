


function draw_pairs_plot(
    price,
    entry_price_long,
    entry_price_short,

    entry_capital_long,
    stop_loss_price_long,
    profit_take_price_long,
    entry_capital_short,
    stop_loss_price_short,
    profit_take_price_short,

){


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
            long_profit_at_take_profit  = entry_capital_long * (profit_take_price_long - entry_price_long) / entry_price_long
            long_loss_at_stop_loss      = entry_capital_long * (entry_price_long - stop_loss_price_long) / entry_price_long
            long_ambition_ratio         = long_profit_at_take_profit / long_loss_at_stop_loss

            
            $("#long_profit_at_take_profit").html(  `profit at profit take: ${long_profit_at_take_profit.toFixed(2)} (${(100 * long_profit_at_take_profit / entry_capital_long).toFixed(1)} %)`)
            $("#long_loss_at_stop_loss").html(      `loss at stop loss:     ${long_loss_at_stop_loss.toFixed(2)}`)
            $("#long_ambition_ratio").html(         `ambition ratio:        ${long_ambition_ratio.toFixed(2)}`)

            valid_long_inputs = (profit_take_price_long > entry_price_long) && (entry_price_long > stop_loss_price_long)
            
            if (valid_long_inputs){
                $("#long_label").removeClass('text-danger')
                $("#long_label").addClass('text-success')
            } else {
                $("#long_label").removeClass('text-success')
                $("#long_label").addClass('text-danger')
                display_toaster({'message': 'Invalid long inputs', 'color': 'red'})
            }
        } else{
                $("#long_label").removeClass('text-danger')
                $("#long_label").removeClass('text-success')

                $("#long_profit_at_take_profit").html(``)
                $("#long_loss_at_stop_loss").html(``)
                $("#long_ambition_ratio").html(``)

        }



        if (short_data_present) {
            short_profit_at_take_profit  = entry_capital_short * (entry_price_short - profit_take_price_short) / entry_price_short
            short_loss_at_stop_loss      = entry_capital_short * (stop_loss_price_short - entry_price_short) / entry_price_short
            short_ambition_ratio         = short_profit_at_take_profit / short_loss_at_stop_loss

            
            $("#short_profit_at_take_profit").html(  `profit at profit take: ${short_profit_at_take_profit.toFixed(2)} (${(100 * short_profit_at_take_profit / entry_capital_short).toFixed(1)} %)`)
            $("#short_loss_at_stop_loss").html(      `loss at stop loss:     ${short_loss_at_stop_loss.toFixed(2)}`)
            $("#short_ambition_ratio").html(         `ambition ratio:        ${short_ambition_ratio.toFixed(2)}`)

            
            // const safe_borrow_amount = (payload.admin_settings.aave_borrow_to_collateral_added_safety_ratio * payload.admin_settings.aave_user_account_data.availableBorrowsBase).toFixed(2)

            // if (entry_capital_short >= safe_borrow_amount){
            //     display_toaster({'message': `you are going to borrow too much. max: ${payload.admin_settings.aave_user_account_data.availableBorrowsBase.toFixed(2)} recommended: ${safe_borrow_amount}`, 'color': 'red'})
            // }


            valid_short_inputs = (profit_take_price_short < entry_price_short) && (entry_price_short < stop_loss_price_short) //&& (entry_capital_short < safe_borrow_amount)

            
            if (valid_short_inputs){
                $("#short_label").removeClass('text-danger')
                $("#short_label").addClass('text-success')

            } else {
                $("#short_label").removeClass('text-success')
                $("#short_label").addClass('text-danger')

                display_toaster({'message': 'Invalid short inputs', 'color': 'red'})
            }

        }else{
                $("#short_label").removeClass('text-danger')
                $("#short_label").removeClass('text-success')

                $("#short_profit_at_take_profit").html(``)
                $("#short_loss_at_stop_loss").html(``)
                $("#short_ambition_ratio").html(``)

        }



        if (valid_long_inputs && valid_short_inputs) {

            let total_profit_if_price_goes_down = (short_profit_at_take_profit - long_loss_at_stop_loss).toFixed(2)
            let total_profit_if_price_goes_up = (long_profit_at_take_profit - short_loss_at_stop_loss).toFixed(2)
            
            $("#total_profit_if_price_goes_down").html(`total profit if price goes down: ${total_profit_if_price_goes_down}`)
            $("#total_profit_if_price_goes_up").html(`total profit if price goes up: ${total_profit_if_price_goes_up}`)

            const start_price = Math.floor(Math.min(stop_loss_price_long, profit_take_price_long, stop_loss_price_short, profit_take_price_short))
            const end_price = Math.floor(Math.max(stop_loss_price_long, profit_take_price_long, stop_loss_price_short, profit_take_price_short))


            let prices = [];
            let long_profits = [];
            let short_profits = [];
            let long_and_short_profits = [];

            for (let price = start_price - 10 ; price < end_price + 10; price += 5) {
                prices.push(price);


                let long_profit = 0;

                if (price < stop_loss_price_long){
                    long_profit = (entry_capital_long * (stop_loss_price_long - entry_price_long) / entry_price_long)
                } else if (price > profit_take_price_long) {
                    long_profit = (entry_capital_long * (profit_take_price_long - entry_price_long) / entry_price_long)
                }
                else {
                    long_profit = (entry_capital_long * (price - entry_price_long) / entry_price_long)
                }

                long_profits.push(long_profit);
                




                let short_profit = 0;

                if (price > stop_loss_price_short){
                    short_profit = (entry_capital_short * (entry_price_short - stop_loss_price_short) / entry_price_short)

                } else if (price < profit_take_price_short) {
                    short_profit = (entry_capital_short * (entry_price_short - profit_take_price_short) / entry_price_short)

                } else {

                    short_profit = (entry_capital_short * (entry_price_short - price) / entry_price_short)
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

            let vertical_base_height = Math.max(Math.abs(short_profit_at_take_profit), Math.abs(long_profit_at_take_profit))
            let vertical_line_height_long  = (entry_capital_long / (entry_capital_short + entry_capital_long)) * vertical_base_height;
            let vertical_line_height_short = (entry_capital_short / (entry_capital_short + entry_capital_long)) * vertical_base_height;

            var layout = {
                shapes: [
                    // Vertical line at entry_price_long
                    {
                        type: 'line',
                        x0: price,
                        x1: price,
                        y0: -vertical_line_height_long,
                        y1: vertical_line_height_long,
                        line: {color: 'black',width: 2}
                    },

                    

                    {
                        type: 'rect',
                        x0: entry_price_long, // Left edge at 25% of the plot width
                        y0: 0, // Bottom edge at 25% of the plot height
                        x1: profit_take_price_long, // Right edge at 75% of the plot width
                        y1: vertical_line_height_long, // Top edge at 75% of the plot height
                        fillcolor: 'rgba(50, 171, 96, 0.3)', // Semi-transparent green fill
                        line: {
                            width: 0
                        }
                    },


                    {
                        type: 'rect',
                        x0: stop_loss_price_long, // Left edge at 25% of the plot width
                        y0: 0, // Bottom edge at 25% of the plot height
                        x1: entry_price_long, // Right edge at 75% of the plot width
                        y1: vertical_line_height_long, // Top edge at 75% of the plot height
                        fillcolor: 'rgba(171, 50, 50, 0.3)', // Semi-transparent green fill
                        line: {
                            width: 0
                        }
                    },


                    // short

                    {
                        type: 'rect',
                        x0: profit_take_price_short, // Left edge at 25% of the plot width
                        y0: 0, // Bottom edge at 25% of the plot height
                        x1: entry_price_short, // Right edge at 75% of the plot width
                        y1: -vertical_line_height_short, // Top edge at 75% of the plot height
                        fillcolor: 'rgba(50, 171, 96, 0.3)', // Semi-transparent green fill
                        line: {
                            width: 0
                        }
                    },


                    {
                        type: 'rect',
                        x0: entry_price_short, // Left edge at 25% of the plot width
                        y0: 0, // Bottom edge at 25% of the plot height
                        x1: stop_loss_price_short, // Right edge at 75% of the plot width
                        y1: -vertical_line_height_short, // Top edge at 75% of the plot height
                        fillcolor: 'rgba(171, 50, 50, 0.3)', // Semi-transparent green fill
                        line: {
                            width: 0
                        }
                    },
                ]
            }

            Plotly.newPlot('new_order_profit_loss_overlook_plot', data, layout);   


        }



    
}