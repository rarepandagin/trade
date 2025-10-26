
function dex_draw_token_arena(payload){
	// Extract x and y values into arrays
	const tokens = payload.admin_settings.tokens.filter(x => x.show_on_chart) 

	


	const xValues = tokens.map(item => item.liquidity);
	const yValues = tokens.map(item => item.volume);
	const labels = tokens.map(item => item.name);
	const links = tokens.map(item => item.url);
	const colors = tokens.map(item => item.epoch_created);

	const image_urls = tokens.map(item => item.image_url);

	// Define the trace for the scatter plot
	const trace = {
		x: xValues,
		y: yValues,
		text: labels,
		hoverinfo: 'text',
		customdata: links,
		// customdata: image_urls,

		// hovertemplate: `
		// 	<b>Point (%{x}, %{y})</b><br>
		// 	<img src="%{customdata}" />
		// 	<extra></extra>
		// `,

		mode:'markers+text',
		type: 'scatter',


		marker: {
			size: 15,
			color: colors, // Use the value array for coloring
			colorscale: 'Blackbody', // Choose a named colorscale
			showscale: true, // Show the colorbar
			cmin: Math.min(...colors), // Set the lower bound of the color domain
			cmax: Math.max(...colors) // Set the upper bound of the color domain
		}


	};

	// Define the layout
	var layout = {
		title: {
			text: 'Token Arena',
			font: {
			family: 'Courier New, monospace',
			size: 24
			},
			xref: 'paper',
			x: 0.05
		},
		xaxis: {
			title: {
			text: 'Liquidity',
			font: {
				family: 'Courier New, monospace',
				size: 18,
				color: '#7f7f7f'
			},

			}
		},
		yaxis: {
			title: {
			text: 'Volume',
			font: {
				family: 'Courier New, monospace',
				size: 18,
				color: '#7f7f7f'
			},

			}
		},

		// plot_bgcolor:"rgba(221, 221, 221, 0.9)",
      	paper_bgcolor:"rgba(192, 192, 192, 0.9)",

	};


	var myPlot = document.getElementById('dex_tokens_arena__plot');
	Plotly.newPlot(myPlot, [trace], layout);

	myPlot.on('plotly_click', function(data) {
	if (data.points.length === 1) {
		var link = data.points[0].customdata;
		window.open(link, '_blank');
	}
	});   

}




function populate_dex_new_tokens_table(payload){
	payload.admin_settings.tokens.sort((a, b) => b.epoch_created - a.epoch_created);

	let html_ = `
	<table class="table">
	<thead>
		<tr>
			<th>Name</th>
			<th>Volume</th>
			<th>Liquidity</th>
			<th>Volume / Makers</th>
			<th>Makers</th>
			<th>Age</th>
			<th>Social</th>
			<th>Security</th>
			
			
			<th></th>
		</tr>
	</thead>
	<tbody>
	`

	payload.admin_settings.tokens.forEach(token => {


		if(token.imported){return;}

		// locked liquidity html

		let locked_liquidity_html = '';

		if (token.locked_liquidity){
			locked_liquidity_html += `<p class="text-success">Locked liquidity</p>`
		} else {
			locked_liquidity_html += `<p class="text-danger">No locked liquidity</p>`
		}


		// security
		const security_cases_true_count = [token.go_security, token.quick_intel, token.token_sniffer, token.honeypot_is].filter(value => value === true).length
		let security_html = ''
		if (security_cases_true_count == 0){
			security_html = 'danger'
		} else if (security_cases_true_count == 1){
			security_html = 'danger'
		} else if (security_cases_true_count == 2){
			security_html = 'danger'
		} else if (security_cases_true_count == 3){
			security_html = 'warning'
		} else if (security_cases_true_count == 4){
			security_html = 'success'
		}
		security_html = `<span class="text-${security_html}">go_security: ${token.go_security}<br>quick_intel: ${token.quick_intel}<br>token_sniffer: ${token.token_sniffer}<br>honeypot_is: ${token.honeypot_is}</span>`


		// social
		const social_cases_true_count = [token.has_website, token.has_twitter, token.has_telegram].filter(value => value === true).length
		let social_html = ''
		if (social_cases_true_count == 0){
			social_html = 'danger'
		} else if (social_cases_true_count == 1){
			social_html = 'warning'
		} else if (social_cases_true_count == 2){
			social_html = 'warning'
		} else if (social_cases_true_count == 3){
			social_html = 'success'
		} 
		social_html = `<span class="text-${social_html}">has_website: ${token.has_website}<br>has_twitter: ${token.has_twitter}<br>has_telegram: ${token.has_telegram}</span>`



		// show_on_chart html

		let show_on_chart_html = ``;
		if (token.show_on_chart) {
			show_on_chart_html = `<button type="button" onclick="dex_toggle_token_on_chart('${token.contract}');" class="btn btn-warning btn-sm m-1">Hide on chart</button>`
		} else {
			show_on_chart_html = `<button type="button" onclick="dex_toggle_token_on_chart('${token.contract}');" class="btn btn-success btn-sm m-1">Show on chart</button>`
		}

		const token_age_seconds = Math.floor(Date.now() / 1000) - token.epoch_created

		html_ += `
		
			<tr>
				<td>
					<img src="${token.image_url}" style="width:64px; height:64px"/>
					<a href ="https://dexscreener.com/ethereum/${token.contract}" target="_blank">${token.name}</a>
					<br>
					contract: ${token.contract}
					<br>
					${locked_liquidity_html}
				</td>

				<td>${token.volume.toLocaleString()}</td>
				<td>${token.liquidity.toLocaleString()}</td>
				<td>${(token.volume / token.makers).toFixed(2)}</td>
				<td>${token.makers}</td>
				<td>${(token_age_seconds / 3600).toFixed(1) } hr</td>
				<td>${social_html}<br>
				<td>${security_html}</td>
				
				<td>
				${show_on_chart_html}
						<button type="button" onclick="dex_hide_token('${token.contract}');" class="btn btn-warning btn-sm m-1">Hide</button>

						<button type="button" onclick="dex_import_token('${token.contract}');" class="btn btn-success btn-sm m-1">Import</button>
				</td>
			</tr>
		`
	});

	html_ += `</tbody></table>`


	$("#dex_trending_tokens__table").html(html_);

}




function populate_dex_imported_tokens_table(payload){
	payload.admin_settings.tokens.sort((a, b) => a.name.localeCompare(b.name));

	let html_ = `
	<table class="table">
	<thead>
		<tr>
			<th>Name</th>
			<th>Price</th>
			<th>Balance</th>
			<th>Buy</th>
			<th>Sell</th>
			<th></th>
		</tr>
	</thead>
	<tbody>
	`


	payload.admin_settings.tokens.forEach(token => {
		if(token.imported){

			let sell_html = ``
			if (token.approved){
				sell_html = `
						<button type="button" onclick="dex_sell_token('${token.contract}', 25);" class="btn btn-success btn-sm m-1">sell 25%</button>
						<button type="button" onclick="dex_sell_token('${token.contract}', 50);" class="btn btn-success btn-sm m-1">sell 50%</button>
						<button type="button" onclick="dex_sell_token('${token.contract}', 100);" class="btn btn-success btn-sm m-1">sell 100%</button>
				`
			} else {
				sell_html = `
						<button type="button" onclick="dex_approve_token('${token.contract}');" class="btn btn-primary btn-sm m-1">approve to sell</button>
						`
			}

			html_ += `
			
				<tr>
					<td>
							<img src="${token.image_url}" style="width:64px; height:64px"/>
						<a href ="https://dexscreener.com/ethereum/${token.contract}" target="_blank">${token.name}</a>
					</td>

					<td>
						<div class="d-flex justify-content-start  gap-2">

							<p>Price: ${token.price}<br>
							Value: ${(token.price * token.balance).toFixed(2)}</p><br>
							<button type="button" onclick="dex_quote_token('${token.contract}');" class="btn btn-primary btn-sm m-1">quote</button>
						</div>
					</td>

					<td>
						<div class="d-flex justify-content-start  gap-2">

							<p>Balance: ${token.balance}</p>

							<button type="button" onclick="dex_check_balance_token('${token.contract}');" class="btn btn-primary btn-sm m-1">check balance</button>
						</div>
					
					</td>
					
					<td>
						<div class="d-flex justify-content-start  gap-2">
							<input  class="form-control form-control-sm" type="number" style="width: 100px;" step="any" id="dex_buy_token_fiat_amount_${token.contract}_input"  value="2" />
							<button type="button" onclick="dex_buy_token('${token.contract}');" class="btn btn-danger btn-sm m-1">buy token</button>
						</div>
					</td>

					<td>
						${sell_html}
					</td>

					<td>
						<button type="button" onclick="dex_remove_import_token('${token.contract}');" class="btn btn-warning btn-sm m-1">remove import</button>
					</td>

				</tr>
			`
		
		}


	})
	
	$("#dex_imported_tokens__table").html(html_);


	}





	
    function dex_scan_for_new_tokens(){ ajax_call('dex_scan_for_new_tokens', {}) };
    function dex_delete_all_tokens(){ ajax_call('dex_delete_all_tokens', {}) };
    function dex_hide_token(token_contract){ ajax_call('dex_hide_token', {'token_contract': token_contract}) };
    function dex_toggle_token_on_chart(token_contract){ ajax_call('dex_toggle_token_on_chart', {'token_contract': token_contract}) };
    function dex_import_token(token_contract){ ajax_call('dex_import_token', {'token_contract': token_contract}) };
    function dex_remove_import_token(token_contract){ ajax_call('dex_remove_import_token', {'token_contract': token_contract}) };
    
    function dex_buy_token(token_contract){ 
		const fiat_amount = $(`#dex_buy_token_fiat_amount_${token_contract}_input`).val();

        ajax_call('dex_buy_token', {'token_contract': token_contract, 'fiat_amount': fiat_amount})
		 
    };

    function dex_sell_token(token_contract, sell_percentage){ 
        ajax_call('dex_sell_token', {'token_contract': token_contract, 'sell_percentage': sell_percentage})
    };

    function dex_check_balance_token(token_contract){ 
        ajax_call('dex_check_balance_token', {'token_contract': token_contract})
    };

    function dex_quote_token(token_contract){
		const quote_fiat_amount =  $(`#quote_fiat_amount__input`).val();
        ajax_call('dex_quote_token', {'token_contract': token_contract, 'quote_fiat_amount': quote_fiat_amount})
    };

    function dex_approve_token(token_contract){
        ajax_call('dex_approve_token', {'token_contract': token_contract})
    };

	function dex_add_token_manually(){
		const new_token_name =  $(`#new_token_name__input`).val();
		const new_token_address =  $(`#new_token_address__input`).val();
		const new_token_contract =  $(`#new_token_contract__input`).val();
        ajax_call('dex_add_token_manually', {'new_token_name': new_token_name, 'new_token_address': new_token_address, 'new_token_contract': new_token_contract})

	}
