

        function bot_draw_data_on_return(returned_payload){

            var format = {year: '2-digit',month: '2-digit', day: '2-digit', hour:'2-digit', minute:'2-digit', second:'2-digit'};
            const X= returned_payload.epoch.map(unix => Intl.DateTimeFormat('en-US', format).format(unix * 1000));
            // const X = returned_payload.epoch
            
            const price = {
                    x: X,
                    y: returned_payload.price,
                    name:'Price', type: 'scatter', mode: 'lines',
                    line: {color: 'rgba(4, 0, 255, 1)', width: 0.4,},
                };

            const ema_20 = {
                    x: X,
                    y: returned_payload.ema_20,
                    name:'ema_20', type: 'scatter', mode: 'lines',
                    line: {width: 0.8,},
                };

            const ema_200 = {
                    x: X,
                    y: returned_payload.ema_200,
                    name:'ema_200', type: 'scatter', mode: 'lines',
                    line: {width: 0.8, color: 'blue', },
                };




            // MACD
            const macd = {
                    x: X,
                    y: returned_payload.macd,
                    name:'macd',
                    type: 'scatter', mode: 'lines', line: {width: 0.8,color: 'blue',},
                    xaxis: 'x2', yaxis: 'y2' 
                };
            const macd_signal = {
                    x: X,
                    y: returned_payload.macd_signal,
                    name:'macd_signal',
                    type: 'scatter', mode: 'lines', line: {width: 0.8,color: 'orange',},
                    xaxis: 'x2', yaxis: 'y2' 
                };
            const macd_histogram = {
                    x: X,
                    y: returned_payload.macd_histogram,
                    name:'macd_histogram',
                    type: 'scatter', mode: 'lines', line: {width: 0.8,color: 'red',},
                    xaxis: 'x2', yaxis: 'y2' 
                };


            // RSI
            const rsi = {
                    x: X,
                    y: returned_payload.rsi,
                    name:'rsi',
                    type: 'scatter', mode: 'lines', line: {width: 0.8,color: 'red',},
                    xaxis: 'x3', yaxis: 'y3' 
                };



            // BB
            const bb_ub = {
                    x: X,
                    y: returned_payload.bb_ub,
                    name:'bb_ub',
                    type: 'scatter', mode: 'lines', line: {width: 0.2,color: 'red',},
                    // xaxis: 'x3', yaxis: 'y3' 
                };
            const bb_lb = {
                    x: X,
                    y: returned_payload.bb_lb,
                    name:'bb_lb',
                    type: 'scatter', mode: 'lines', line: {width: 0.2,color: 'green',},
                    // xaxis: 'x3', yaxis: 'y3' 
                };






            const data = [
                price,
                ema_20,
                ema_200,

                macd,
                macd_signal,
                macd_histogram,

                // rsi,
                bb_lb,
                bb_ub,
            ];

            const layout = {
                height: 1800,
                width: 1400,

                grid: {
                    rows: 3,
                    columns: 1,
                    pattern: 'independent',
                    shared_xaxes: true
                },
                yaxis: { title: 'Top Subplot Y-Axis' },
                yaxis2: { title: 'Bottom Subplot Y-Axis' },
                yaxis3: { title: 'Bottom Subplot Y-Axis' },
            };

            Plotly.newPlot('bot_price_plot', data, layout);   
        }







function bot_draw_on_return_anychart(payload){
        
    $("#anychart_chart_container").html("")

    candle_chart_data = "'Date,Open,High,Low,Close,Volume,ema_20"

    payload.chart_df.forEach(x=>{
        candle_chart_data += `\n${x.epoch_open}000,${x.open},${x.high},${x.low},${x.close},${x.volume},${x.ema_20}`
    })
	const x = payload.chart_df.slice(-1);
	candle_chart_data += `\n${x.epoch_open}000,${x.open},${x.high},${x.low},${x.close},${x.volume},${x.ema_20}`

    candle_chart_data += "'"

	// console.log(candle_chart_data)


	var dataTable = anychart.data.table();

	dataTable.addData(candle_chart_data);

	var mapping_candlestick = dataTable.mapAs({
	open: 1,
	high: 2,
	low: 3,
	close: 4
	});

	var chart = anychart.stock();

	var plot = chart.plot(0);

	var series_candlestick = plot.candlestick(mapping_candlestick);
	series_candlestick.name('ETHUSDC');







	var mapping_ema_20 = dataTable.mapAs({x:0, value: 6});
	var firstSeries = plot.line(mapping_ema_20);
	firstSeries.name('EMA 20');

	
	

      // Annotations
      var controller = plot.annotations();

        controller.horizontalLine({
            valueAnchor: payload.admin_settings.prices.weth,
            stroke: "1 rgb(160, 166, 255)"
        });

        // payload.positions_dict.forEach(position => {
        //     if (position.coin === coin){
        //         if (position.display_on_chart){
        //         if (position.active){
                    
        //             controller.horizontalLine({
        //                 valueAnchor: position.entry_price,
        //                 stroke: "1 #0011ffff"
        //             });

        //             controller.horizontalLine({
        //                 valueAnchor: position.stop_loss_price,
        //                 stroke: "1 #ff0000ff"
        //             });
        //             controller.horizontalLine({
        //                 valueAnchor: position.profit_take_price,
        //                 stroke: "1 #48ff00ff"
        //             });


        //         }
        //         }
        //     }
        // })


    chart.background().fill("#1e1e1e"); // Dark background
    chart.background().stroke("#333");  // Border


	chart.title('ETHUSDC');

	chart.width("1200");
	chart.height("800");

	chart.container('anychart_chart_container');

	chart.draw();

    }