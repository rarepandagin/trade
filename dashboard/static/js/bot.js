

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
		const indicator_values = payload.admin_settings.INDICATORS.map(key => x[key]).join(", ");

        candle_chart_data += `\n${x.epoch_open}000,${x.open},${x.high},${x.low},${x.close},${x.volume},${indicator_values}`
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
	chart.padding(60);

	var plot_0 = chart.plot(0);
	plot_0.yAxis().orientation("right");   
	plot_0.height(600);

	// var extraYAxis = plot_0.yAxis(1);
	// extraYAxis.orientation("right");
	// plot_0.yAxis().labels().width(200);


	var series_candlestick = plot_0.candlestick(mapping_candlestick);
	series_candlestick.name('ETHUSDC');





	// for (let i = 6; i < payload.admin_settings.INDICATORS.length-4; i++) {
	// 	const mapping = dataTable.mapAs({x:0, value: i});
	// 	var firstSeries = plot.line(mapping);
	// 	firstSeries.name(payload.admin_settings.INDICATORS[i]);

	// }

	var series = plot_0.line(dataTable.mapAs({x:0, value: 6 + payload.admin_settings.INDICATORS.indexOf('ema_20')}));
	series.name('EMA 20').stroke({color: "#ffc468",  thickness: 0.75,});
	
	series = plot_0.line(dataTable.mapAs({x:0, value: 6 + payload.admin_settings.INDICATORS.indexOf('ema_200')}));
	series.name('EMA 200').stroke({color: "#ff0000",  thickness: 0.75,});

	
	series = plot_0.line(dataTable.mapAs({x:0, value: 6 + payload.admin_settings.INDICATORS.indexOf('bb_ub')}));
	series.name('BB UB').stroke({color: "#a1b3ff", dash: "15 5", thickness: 0.5,});

	
	series = plot_0.line(dataTable.mapAs({x:0, value: 6 + payload.admin_settings.INDICATORS.indexOf('bb_lb')}));
	series.name('BB LB').stroke({color: "#a1b3ff", dash: "15 5", thickness: 0.5,});

	
	

		// Annotations
		var controller = plot_0.annotations();

		controller.horizontalLine({
			valueAnchor: payload.admin_settings.prices.weth,
		stroke: {color: "#f5ff00", dash: "5 5", thickness: 1, opacity: 0.35},
		});

		




	///////////////////////////////////////////////////

	var plot_1 = chart.plot(1);
	plot_1.height(200);
	plot_1.yAxis().orientation("right");   

	// var extraYScale = anychart.scales.linear();
	// plot_1.yAxis(0).enabled(false);

	// var extraYAxis = plot_1.yAxis(1);
	// extraYAxis.orientation("right");
	// extraYAxis.scale(extraYScale); // Assign a custom scale if needed

	series = plot_1.line(dataTable.mapAs({x:0, value: 6 + payload.admin_settings.INDICATORS.indexOf('macd')}));
	series.name('MACD').stroke({color: "#a1b3ff", dash: "5 1", thickness: 0.5,});

	series = plot_1.line(dataTable.mapAs({x:0, value: 6 + payload.admin_settings.INDICATORS.indexOf('macd_signal')})); series.name('MACD Signal');
	series.stroke({color: "#a1b3ff", dash: "5 1", thickness: 0.5,});

	series = plot_1.column(dataTable.mapAs({x:0, value: 6 + payload.admin_settings.INDICATORS.indexOf('macd_histogram')})); series.name('MACD Histogram');
	series.negativeFill("#d50000");  // Red for negative
	series.fill("#0ed500");          // Green for positive   


	// Annotations
	var controller_1 = plot_1.annotations();

	controller_1.horizontalLine({
		valueAnchor: 0,
		stroke: {color: "#f5ff00", dash: "5 5", thickness: 1, opacity: 0.35},
	});



	///////////////////////////////////////////////////
	var plot_2 = chart.plot(2);
	plot_2.height(200);
	plot_2.yAxis().orientation("right");   


	series = plot_2.line(dataTable.mapAs({x:0, value: 6 + payload.admin_settings.INDICATORS.indexOf('rsi')}));
	series.name('RSI').stroke({color: "#a1b3ff", dash: "5 1", thickness: 0.5,});

	series = plot_2.line(dataTable.mapAs({x:0, value: 6 + payload.admin_settings.INDICATORS.indexOf('rsi_smooth')}));
	series.name('RSI Smooth').stroke({color: "#e8ff56",  thickness: 0.5,});

	// Annotations
	var controller_2 = plot_2.annotations();


	controller_2.horizontalLine({
		valueAnchor: 70,
		stroke: {color: "#ffffff", dash: "5 5", thickness: 1, opacity: 0.35},
	});

	controller_2.horizontalLine({
		valueAnchor: 50,
		stroke: {color: "#f5ff00", dash: "5 5", thickness: 1, opacity: 0.35},
	});


	controller_2.horizontalLine({
		valueAnchor: 30,
		stroke: {color: "#ffffff", dash: "5 5", thickness: 1, opacity: 0.35},
	});




	///////////////////////////////////////////////////
	var plot_3 = chart.plot(3);
	plot_3.height(200);
	plot_3.yAxis().orientation("right");   


	series = plot_3.line(dataTable.mapAs({x:0, value: 6 + payload.admin_settings.INDICATORS.indexOf('adx')}));
	series.name('ADX').stroke({color: "#f3364a",  thickness: 0.5,});

	series = plot_3.line(dataTable.mapAs({x:0, value: 6 + payload.admin_settings.INDICATORS.indexOf('pdi')}));
	series.name('+DI').stroke({color: "#4336f3", dash: "5 1", thickness: 0.5,});

	series = plot_3.line(dataTable.mapAs({x:0, value: 6 + payload.admin_settings.INDICATORS.indexOf('ndi')}));
	series.name('-DI').stroke({color: "#f3a136", dash: "5 1", thickness: 0.5,});

	// Annotations
	// var controller_2 = plot_3.annotations();


	// controller_2.horizontalLine({
	// 	valueAnchor: 70,
	// 	stroke: {color: "#ffffff", dash: "5 5", thickness: 1, opacity: 0.35},
	// });






	/////////////////////////////////////////////////// AROON
	var plot_4 = chart.plot(4);
	plot_4.height(200);
	plot_4.yAxis().orientation("right");   


	series = plot_4.line(dataTable.mapAs({x:0, value: 6 + payload.admin_settings.INDICATORS.indexOf('aroon_up')}));
	series.name('Aroon Up').stroke({color: "#fb912b",  thickness: 0.5,});

	series = plot_4.line(dataTable.mapAs({x:0, value: 6 + payload.admin_settings.INDICATORS.indexOf('aroon_down')}));
	series.name('Aroon Down').stroke({color: "#4336f3", dash: "5 1", thickness: 0.5,});






	/////////////////////////////////////////////////// Stochastic
	var plot_5 = chart.plot(5);
	plot_5.height(200);
	plot_5.yAxis().orientation("right");   


	series = plot_5.line(dataTable.mapAs({x:0, value: 6 + payload.admin_settings.INDICATORS.indexOf('so_percent_k')}));
	series.name('Stochastic K').stroke({color: "#3df336",  thickness: 0.5,});

	series = plot_5.line(dataTable.mapAs({x:0, value: 6 + payload.admin_settings.INDICATORS.indexOf('so_percent_d')}));
	series.name('Stochastic D').stroke({color: "#f3364a", dash: "5 1", thickness: 0.5,});


	// Annotations
	var controller_5 = plot_5.annotations();


	controller_5.horizontalLine({
		valueAnchor: 80,
		stroke: {color: "#ffffff", dash: "5 5", thickness: 1, opacity: 0.35},
	});


	controller_5.horizontalLine({
		valueAnchor: 20,
		stroke: {color: "#ffffff", dash: "5 5", thickness: 1, opacity: 0.35},
	});




	/////////////////////////////////////////////////// OBV
	var plot_6 = chart.plot(6);
	plot_6.height(200);
	plot_6.yAxis().orientation("right");   


	series = plot_6.line(dataTable.mapAs({x:0, value: 6 + payload.admin_settings.INDICATORS.indexOf('obv')}));
	series.name('OBV').stroke({color: "#3df336",  thickness: 0.5,});




	/////////////////////////////////////////////////// Ichimoku
	var plot_7 = chart.plot(7);
	plot_7.height(200);
	plot_7.yAxis().orientation("right");   


	series = plot_7.line(dataTable.mapAs({x:0, value: 6 + payload.admin_settings.INDICATORS.indexOf('ichimoku_conversion_line')}));
	series.name('Conversion Line').stroke({color: "#3df336",  thickness: 0.5,});


	series = plot_7.line(dataTable.mapAs({x:0, value: 6 + payload.admin_settings.INDICATORS.indexOf('ichimoku_base_line')}));
	series.name('Base Line').stroke({color: "#f33636",  thickness: 0.5,});

	series = plot_7.line(dataTable.mapAs({x:0, value: 6 + payload.admin_settings.INDICATORS.indexOf('ichimoku_leading_span_a')}));
	series.name('Span A').stroke({color: "#bbfab5",  thickness: 0.5,});


	series = plot_7.line(dataTable.mapAs({x:0, value: 6 + payload.admin_settings.INDICATORS.indexOf('ichimoku_leading_span_b')}));
	series.name('Span B').stroke({color: "#f2b5fa",  thickness: 0.5,});


	// series = plot_7.line(dataTable.mapAs({x:0, value: 6 + payload.admin_settings.INDICATORS.indexOf('ichimoku_lagging_span')}));
	// series.name('Lagging').stroke({color: "#48f336",  thickness: 0.5,});









    chart.background().fill("#1e1e1e"); // Dark background
    chart.background().stroke("#333");  // Border


	chart.title('ETHUSDC');

	chart.width( "100%");
	chart.height("2000");

	chart.container('anychart_chart_container');

	chart.draw();

}



function populate_indicators_table(payload){

	let indicators_table__head_html = '<th></th>'

	payload.admin_settings.MINUTES.forEach(MINUTE=>{
		indicators_table__head_html += `<th>${MINUTE}</th>`
	})

	$("#indicators_table__head").html(indicators_table__head_html);


	let indicators_table__body_html = ''

	let indicator_row_html = `<td></td>`

	payload.admin_settings.MINUTES.forEach(MINUTE=>{
		indicator_row_html += `<td>
		EMA:<br>
		slow: ${payload.admin_settings.vision.ema_lag_direction[MINUTE]['slow']}<br>
		fast: ${payload.admin_settings.vision.ema_lag_direction[MINUTE]['fast']}<br>
		lineup: ${payload.admin_settings.vision.ema_lineup[MINUTE]}<br>
		price is ${payload.admin_settings.vision.ema_200_comparison[MINUTE]} ema_200<br>
		
		</td>`
	})
	indicator_row_html = `<tr>${indicator_row_html}<tr>`
	indicators_table__body_html += indicator_row_html



	payload.admin_settings.INDICATORS.forEach(INDICATOR=>{
		
		indicator_row_html = ``



		payload.admin_settings.MINUTES.forEach(MINUTE=>{
				const v = payload.admin_settings.live_indicators[`minutes_${MINUTE}`][INDICATOR]['v'];
				const d = payload.admin_settings.live_indicators[`minutes_${MINUTE}`][INDICATOR]['d'];
				indicator_row_html +=  `<td>${v}`

				if ((INDICATOR.includes('ema')) || (INDICATOR.includes('macd'))){
					if (d>=0) {
						indicator_row_html +=  `<span class="ms-1 triangle_up"></span>`
					}
					else {
						indicator_row_html +=  `<span class="ms-1 triangle_down"></span>`
					}
				}
				
				
				indicator_row_html += `</td>`
				
		})

		indicator_row_html = `<tr><td>${INDICATOR}</td>${indicator_row_html}<tr>`
		indicators_table__body_html += indicator_row_html

	})

	
	$("#indicators_table__body").html(indicators_table__body_html);

}


function get_observation_html(observation, bias, trade){
	let ret = ` `

	const minutes = observation.table[trade][bias];

	if (minutes.length > 1){
		ret += `<span class="text-warning">X${minutes.length} </strong></span>`
	}

	if (minutes.some(item => item.includes('strong'))) {
		ret += `<span class="text-warning"><strong> (Strong) </strong></span>`
	}	

	
	// ret += ` - ${observation.description}`;
	ret += ` - ${observation.description} <span class="small">(${minutes.toString()})</span>`;

	ret += `<br>`
	return ret
}
function populate_observation_divs(payload){

	let pro_long_html = ``
	payload.admin_settings.vision.observations_pro_long.forEach(observation=>{
		pro_long_html += get_observation_html(observation, 'pro', 'long')
	})

	let pro_short_html = ``
	payload.admin_settings.vision.observations_pro_short.forEach(observation=>{
		pro_short_html += get_observation_html(observation, 'pro', 'short')
	})

	let against_long_html = ``
	payload.admin_settings.vision.observations_against_long.forEach(observation=>{
		against_long_html += get_observation_html(observation, 'against', 'long')
	})

	let against_short_html = ``
	payload.admin_settings.vision.observations_against_short.forEach(observation=>{
		against_short_html += get_observation_html(observation, 'against', 'short')
	})

	$("#pro_long_observations__div").html(pro_long_html);
	$("#against_long_observations__div").html(against_long_html);

	$("#pro_short_observations__div").html(pro_short_html);
	$("#against_short_observations__div").html(against_short_html);

}