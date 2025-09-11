
function update_depth_chart(payload){


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

        layout.xaxis.dtick = 2 * payload.admin_settings.depth_cluster_width_usd;
    }
    const config = {responsive: true};

    // Create the plot
    Plotly.newPlot('orderBookPlot', data, layout, config);

}