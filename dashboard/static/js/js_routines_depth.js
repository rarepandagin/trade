
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
      width: 1500,
      height: 600,
      xaxis: {
        title: 'Price',
        range: [payload.admin_settings.depth_lowest_price, payload.admin_settings.depth_highest_price],
        tickmode: 'linear',
        
        // The order of categories on the x-axis can be controlled
        // For a clean order, you might want to sort the data
        // The default is "trace", which uses the order in the data array
        // You can also use "category ascending" or "category descending"
        // to sort by the x-values
        categoryorder: 'category ascending' // Sorts from lowest to highest price
      },
      yaxis: {
        title: 'Volume'
      },
      // The drawing order of traces is determined by their order in the data array
      // The last trace in the array is drawn on top
      // To ensure asks are on top of bids, place the asks trace last
      // This is already the case in the data array above
      barmode: 'overlay' // Overlap the bars to show the order book structure
    };

    if (payload.admin_settings.depth_filtering_active){
        data[0].width = payload.admin_settings.depth_cluster_width_usd;
        data[1].width = payload.admin_settings.depth_cluster_width_usd;

        layout.xaxis.dtick = payload.admin_settings.depth_cluster_width_usd;
    }

    // Create the plot
    Plotly.newPlot('orderBookPlot', data, layout);

}