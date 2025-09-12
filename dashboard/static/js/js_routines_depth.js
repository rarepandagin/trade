
function draw_depth_bar_plot(payload){

    const bids = payload.bids
    const asks = payload.asks

    // Prepare data for Plotly
    const data = [
      // Bids (left side, green bars)
      {
        x: bids.map(bid => bid[0]), // Negative prices for left side
        y: bids.map(bid => bid[1]),
        type: 'bar',
        name: 'Bids',
        marker: { color: 'green' },
        orientation: 'v' // Vertical bars
      },
      // Asks (right side, red bars)
      {
        x: asks.map(ask => ask[0]), // Positive prices for right side
        y: asks.map(ask => ask[1]),
        type: 'bar',
        name: 'Asks',
        marker: { color: 'red' },
        orientation: 'v' // Vertical bars
      }
    ];

    // Layout configuration
    const layout = {
      title: 'Order Book',
      template: 'plotly_dark',
      plot_bgcolor: 'rgba(0, 0, 0, 1)',  
      paper_bgcolor: '#000000ff'   ,

      margin: {l: 50, r: 100, b: 50, t: 50, pad: 4},

      xaxis: {
        title: 'Price',
        range: [payload.admin_settings.depth_lowest_price, payload.admin_settings.depth_highest_price],
        tickmode: 'linear',
        color: 'white',
        
        categoryorder: 'category ascending' 
      },
      yaxis: {
        title: 'Volume',
        color: 'white',

      },
      barmode: 'overlay' 
    };

    if (payload.admin_settings.depth_filtering_active){
        data[0].width = payload.admin_settings.depth_cluster_width_usd;
        data[1].width = payload.admin_settings.depth_cluster_width_usd;

        layout.xaxis.dtick = 4 * payload.admin_settings.depth_cluster_width_usd;
    }
    const config = {responsive: true};

    // Create the plot
    Plotly.newPlot('orderBookBarPlot', data, layout, config);

}

function draw_depth_pie_plot(payload){

    var data = [{
      type: "pie",
      values: [payload.best_bid_volume, payload.best_ask_volume], // Example values
      labels: ["Bid", "Ask"], // Corresponding labels
      marker: {
        colors: ['#00862dff', '#a30000ff'] // Custom colors for the slices
      },
	textinfo: "label+percent", // Display label and percentage
      textposition: "inside" // Position text inside the slices
    }];

    var layout = {
      height: 400,
      width: 400,
	plot_bgcolor: 'rgba(0, 0, 0, 1)',  

      margin: {"t": 0, "b": 0, "l": 0, "r": 0},
      showlegend: false // Optional: hide the legend
    };

    Plotly.newPlot('orderBookPiePlot', data, layout);

}


function draw_depth_series_plot(payload){


    var trace1 = { 
      x: payload.ticks.map(x=>x['epoch']), 
      y: payload.ticks.map(x=>x['data']['price']), 
      mode: 'lines', 
      name: 'Price',
      type: 'scatter' ,
        line: {
          color: 'rgba(0, 0, 0, 1)',
          width: 3
        }
    };

    var trace2 = { 
      x: payload.ticks.map(x=>x['epoch']), 
      y: payload.ticks.map(x=>x['data']['best_ask_price']), 
      mode: 'lines+markers', 
      name: 'best_ask_price',
      type: 'scatter' ,
      line: {
          color: 'rgba(255, 0, 0, 1)',
          width: 1
        },
      error_y: {
        type: 'data',
        array: payload.ticks.map(x=>x['data']['best_ask_volume']/ 900),
        visible: true,
          thickness: 1,
          width: 1,
      }
    };

    var trace3 = { 
      x: payload.ticks.map(x=>x['epoch']), 
      y: payload.ticks.map(x=>x['data']['best_bid_price']), 
      mode: 'lines', 
      name: 'best_bid_price',
      type: 'scatter' ,
      line: {
          color: 'rgba(4, 0, 255, 1)',
          width: 1,

      },
      error_y: {
        type: 'data',
        array: payload.ticks.map(x=>x['data']['best_bid_volume']/ 900),
        visible: true,
          thickness: 1,
          width: 1,
      }
    };

    var data = [trace1, trace2, trace3];

    var layout = { 
      margin: {l: 150, r: 100, b: 50, t: 50, pad: 4},
      width:1500,

      xaxis: { title: { text: 'X-axis' } },
      yaxis: { title: { text: 'Y-axis' } }
    };
    const config = {responsive: true};

    Plotly.newPlot('orderBookSeriesPlot', data, layout, config);   



}


function update_depth_chart(payload){


	draw_depth_bar_plot(payload);
	// draw_depth_pie_plot(payload);
	draw_depth_series_plot(payload);



    $("#best_bid_price").html(payload.best_bid_price);
    $("#best_ask_price").html(payload.best_ask_price);
    $("#best_bid_volume").html(payload.best_bid_volume);
    $("#best_ask_volume").html(payload.best_ask_volume);


}