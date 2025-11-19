async function copy_to_clipboard(text) {
  // Try using the modern async Clipboard API
  if (navigator.clipboard) {
    try {
      await navigator.clipboard.writeText(text);
    } catch (err) {
      console.error('Failed to copy: ', err);
    }
  } else {
  }
}




class Token {

	constructor(token_dict){
		Object.assign(this, token_dict);
	}

	get_basic_html(){

		let locked_liquidity_html = ``

		

		// locked_liquidity_html += `<button type="button" class="btn btn-secondary btn-sm disable_while_busy m-1" style="height: 30px;" onclick="copy_to_clipboard('${this.contract}')">copy contract</button>`


		
		if(this.locked > 0) {

			let lock_lock_until = this.lock_epoch_end_lock - Math.floor(Date.now() / 1000)

			if (lock_lock_until > 0){


				let lock_platform_url = ``
				switch(this.lock_platform) {
					case 'uncx':
						lock_platform_url=`https://beta.uncx.network/lockers/univ2/chain/1/address/${this.pair_address}/lock/0`
						break;
					case 'pink':
						lock_platform_url=`https://legacy.pinksale.finance/pinklock/detail/${this.pair_address}?chain=ETH`
						break;
					case 'gempad':
						lock_platform_url=`https://gempad.app/locks?tab=0&q=${this.contract}`
						break;
					default:
						break;
				}   

				locked_liquidity_html += `
					<br>
					<span class="badge rounded-pill bg-success fs-7 m-1">
						locked on ${this.lock_platform}
					</span>
					<br>
					<a href="${lock_platform_url}" target="_blank" >
					<img src="https://unrealizer-statics.s3.eu-central-1.amazonaws.com/lock.png"/>
					until ${readable_elapsed_delta_epochs(lock_lock_until)}
					</a>
				`
			}

		}

		let html = `
		
			<a class="h5" href ="https://www.dextools.io/app/en/ether/pair-explorer/${this.contract}" target="_blank" >${this.name}</a>
			<div class="vstack  mt-1">
				<a href ="https://www.dextools.io/app/en/ether/pair-explorer/${this.contract}" 	target="_blank" >Dex Tools</a>
				<a href ="https://dexscreener.com/ethereum/${this.contract}" 					target="_blank" >Dex Screener</a>
				<a href ="https://tokensniffer.com/bubble/v2/eth/${this.contract}" 				target="_blank" >Token Sniffer</a>
				<br>
				<a href ="https://gopluslabs.io/token-security/1/${this.contract}" 				target="_blank" >Go plus</a>
				<a href ="https://app.quickintel.io/scanner?type=token&chain=eth&contractAddress=${this.contract}" target="_blank" >Quick Intel</a>
				<a href ="https://honeypot.is/ethereum?address=${this.contract}" target="_blank" >Honey Pot</a>
			</div>
			${locked_liquidity_html}
		
		`


		return html

	}


	get_age_html(){
		const token_age_seconds = Math.floor(Date.now() / 1000) - this.pair_creation_epoch

		let html = `${readable_elapsed_delta_epochs(token_age_seconds)}`

		return html
	}


	get_pair_html(){

		let html = ``


		this.go_plus_holders.forEach(x=>{
			let color;
			if(x=='UniswapV2'){
				color = 'primary'
			} else {
				color = 'success'
			}
			html+=`<span class="badge rounded-pill bg-${color} fs-7">${x}</span><br>`
		})

		
		html += `
			<a class="m-1" href="https://etherscan.io/address/${this.pair_address}" target="_blank">
				 <span class="badge rounded-pill bg-primary fs-6 m-1">pooled ${(this.weth_pair_reserves).toFixed(2)} weth</span>
			</a><br>`

		let sub_html
		if ((this.go_plus_locked_lp_ratio>0) && (this.lock_pool_lock_ratio > 0)){
			sub_html = `success`
		} else if ((this.go_plus_locked_lp_ratio>0) || (this.lock_pool_lock_ratio > 0)){
			sub_html = `warning`
		} else {
			sub_html = `danger`
		}
		
		html += `

			<span class="badge rounded-pill bg-${sub_html} fs-6 m-1">g+ dex liquidity: ${(2 * this.go_plus_dex_liquidity / 1000).toFixed(0)} K</span>
		`

		html += `
			<br>
			price / weth:<br><span class="text-info">${this.price_per_weth}</span>
		`

		return html;
	}


	get_investigation_html(){

		let status_html = ``

		if (this.investigated){
			status_html += `<p><b>Fully investigated</b> (${this.investigated_count} times)</p>`

		} else {
			status_html += `<p class="text-warning">investigated ${this.investigated_count} times</p>`
		}



		if (this.keep_investigating){
			status_html += `<p class="small">Being re-investigated for weth reserves...</p>`
		}
		
		if (this.investigation_pass){
			status_html += `<p class="text-success elementToFade fs-4">PASS</p>`
		}

		if (this.investigation_safe){
			status_html += `<p class="text-warning elementToFade fs-4">SAFE</p>`
		}

		if (this.investigation_red_flag){
			status_html += `<p class="text-danger  elementToFade fs-4">Red flag ${this.red_flag_reason}</p>`
		}




		return status_html;
		
	}


	
	get_security_html(){

		// security
		const security_cases_true_count = this.go_plus_security_issues.length
		let security_html = ''
		if (security_cases_true_count == 0){
			security_html = 'success'
		} else {
			security_html = 'danger'
		}
		security_html = `<span class="text-${security_html}">${createListFromStrings(this.go_plus_security_issues)}</span>`

		return security_html
	}

	get_volume_html(){
		let html = ``
		html += `${this.volume.toLocaleString()}`
		return html
	}

	get_social_html(){

				const social_cases_true_count = [this.has_website, this.has_twitter, this.has_telegram].filter(value => value === true).length
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
		social_html = `<span class="text-${social_html}">has_website: ${this.has_website}<br>has_twitter: ${this.has_twitter}<br>has_telegram: ${this.has_telegram}</span>`

		return social_html

	}

	get_manual_test_html(){
	
		let html = ``
		
		html += `<button type="button" onclick="dex_token_manual_tests('${this.contract}');" class="btn btn-primary btn-sm m-1">manual tests</button>`
		html += `<button type="button" onclick="dex_token_reinvestigate('${this.contract}');" class="btn btn-primary btn-sm m-1">reinvestigate</button>`
	

		if (this.manual_tests != '{}'){
			const manual_tests = JSON.parse(this.manual_tests)
			html += `
				<br>
				buyers_funding_addresses_entropy: ${manual_tests.buyers_funding_addresses_entropy}<br>
				trade_timing_traffic: ${manual_tests.trade_timing_traffic}
			
			`
		}

		return html;
	}
}


function createListFromStrings(strings) {
	try{
		let html = '<ul>'
		strings.forEach(str => {
			html += `<li>${str}</li>`
		});
		html += `</ul>`
		return html;
	} catch {
		return ''
	}
}


function readable_elapsed_delta_epochs(delta_epochs){
	const day = 24 * 60 * 60
	const hour = 60 * 60
	const minute = 60

	if (delta_epochs > day){
		return `${Math.floor(delta_epochs / day)} days`
	} else if (delta_epochs > hour) {
		return `${Math.floor(delta_epochs / hour)} hours`
	} else if (delta_epochs > minute) {
		return `${Math.floor(delta_epochs / minute)} minutes`
	}
}


function dex_draw_token_arena(payload){
	// Extract x and y values into arrays
	const tokens = payload.admin_settings.tokens.filter(x => x.show_on_chart) 

	


	const xValues = tokens.map(item => item.liquidity);
	const yValues = tokens.map(item => item.volume);
	const labels = tokens.map(item => item.name);
	const links = tokens.map(item => item.symbol);
	const colors = tokens.map(item => item.pair_creation_epoch);


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
	
	
	payload.admin_settings.tokens = payload.admin_settings.tokens.filter(x=>x.show===true)
	payload.admin_settings.tokens.sort((a, b) => b.pair_creation_epoch - a.pair_creation_epoch);

	let tokens = []

	payload.admin_settings.tokens.forEach(x=>tokens.push(new Token(x)))
	



	let html_ = `
	<table class="table">
	<thead>
		<tr>
			<th>Name</th>
			<th>Status</th>
			<th>Pair</th>
			<th>Volume</th>
			<th>Age</th>
			<th>Security</th>
			
			
			<th></th>
			<th></th>
		</tr>
	</thead>
	<tbody>
	`

	tokens.forEach(token => {


		if(token.imported){return;}


		let show_on_chart_html = ``;
		// if (token.show_on_chart) {
		// 	show_on_chart_html = `<button type="button" onclick="dex_toggle_token_on_chart('${token.contract}');" class="btn btn-warning btn-sm m-1">Hide on chart</button>`
		// } else {
		// 	show_on_chart_html = `<button type="button" onclick="dex_toggle_token_on_chart('${token.contract}');" class="btn btn-success btn-sm m-1">Show on chart</button>`
		// }

		html_ += `
		
			<tr>
				<td>
					${token.get_basic_html()}
				</td>

				<td>${token.get_investigation_html()}</td>
				<td>${token.get_pair_html()}</td>

				<td>${token.get_volume_html()}</td>
				<td>${token.get_age_html()}</td>
				<td>${token.get_security_html()}</td>
				
				<td>
				${show_on_chart_html}
						<button type="button" onclick="dex_set_token_as_red_flag('${token.contract}');" class="btn btn-danger btn-sm m-1">Set as red flag</button>

						<button type="button" onclick="dex_import_token('${token.contract}');" class="btn btn-success btn-sm m-1">Import</button>
				</td>

				<td>
					${token.get_manual_test_html()}
				</td>

			</tr>
		`
	});

	html_ += `</tbody></table>`


	$("#dex_trending_tokens__table").html(html_);

}




function populate_dex_imported_tokens_table(payload){

	payload.admin_settings.tokens.sort((a, b) => b.pair_creation_epoch - a.pair_creation_epoch);

	let tokens = []

	payload.admin_settings.tokens.forEach(x=>tokens.push(new Token(x)))


	const weth_price =payload.admin_settings.prices.weth
	
	let html_ = `
	<table class="table">
	<thead>
		<tr>
			<th>Name</th>
			<th>Info</th>
			<th>Balance</th>
			<th>Buy</th>
			<th>Sell</th>
			<th></th>
		</tr>
	</thead>
	<tbody>
	`


	tokens.forEach(token => {
		if(token.imported){

			let sell_html = ``
			if (token.approved){
				sell_html = `
				<div class="vstack">
						<button type="button" onclick="dex_sell_token('${token.contract}', 25);" class="btn btn-success btn-sm m-1">sell 25%</button>
						<button type="button" onclick="dex_sell_token('${token.contract}', 50);" class="btn btn-success btn-sm m-1">sell 50%</button>
						<button type="button" onclick="dex_sell_token('${token.contract}', 100);" class="btn btn-success btn-sm m-1">sell 100%</button>
				</div>
						`
			} else {
				sell_html = `
						<button type="button" onclick="dex_approve_token('${token.contract}');" class="btn btn-primary btn-sm m-1">approve to sell</button>
						`
			}

			html_ += `
			
				<tr>
					<td>
						${token.get_basic_html()}
					</td>
					<td>
						${token.get_age_html()}<br>
						${token.get_pair_html()}<br><br>
						${token.get_investigation_html()}<br>
						${token.get_security_html()}<br>

					</td>

					<td>
						<div class="vstack  gap-2">
							<p>Balance: ${token.balance}</p>


							<p>Value: ${(token.price_per_weth * token.balance).toFixed(15)} WETH</p>
							<p>Value: ${(token.price_per_weth * token.balance * weth_price).toFixed(12)} $</p>
							<button type="button" onclick="dex_check_balance_token('${token.contract}');" class="btn btn-primary btn-sm m-1">check balance</button>

							</div>
					</td>

					
					<td>
						<div>
							<div class="d-flex justify-content-start  gap-2">

								<input class="form-control form-control-sm" type="number" style="width: 80px;" id="dex_buy_token_fiat_amount__input" value="5" />
								<p class="mt-2">usd</p>
							</div>

							<button type="button" onclick="dex_buy_token_by_fiat_amount('${token.contract}')" class="btn btn-danger btn-sm m-1">buy token</button>
						</div>
					</td>

					<td>
						${sell_html}
					</td>

					<td>
						<button type="button" onclick="dex_remove_import_token('${token.contract}');" class="btn btn-warning btn-sm m-1">remove import</button>
					</td>

					<td>
						${token.get_manual_test_html()}

												<button type="button" onclick="dex_set_token_as_red_flag('${token.contract}');" class="btn btn-danger btn-sm m-1">Set as red flag</button>

					</td>

				</tr>
			`
		
		}


	})
	
	$("#dex_imported_tokens__table").html(html_);


	}





	
    function dex_delete_all_tokens(){ ajax_call('dex_delete_all_tokens', {}) };
    function dex_delete_all_tokens(){ ajax_call('dex_delete_all_tokens', {}) };
    function dex_hide_token(token_contract){ ajax_call('dex_hide_token', {'token_contract': token_contract}) };
    function dex_toggle_token_on_chart(token_contract){ ajax_call('dex_toggle_token_on_chart', {'token_contract': token_contract}) };
    function dex_import_token(token_contract){ ajax_call('dex_import_token', {'token_contract': token_contract}) };
    function dex_remove_import_token(token_contract){ ajax_call('dex_remove_import_token', {'token_contract': token_contract}) };
    function dex_token_manual_tests(token_contract){ ajax_call('dex_token_manual_tests', {'token_contract': token_contract}) };
    function dex_token_reinvestigate(token_contract){ ajax_call('dex_token_reinvestigate', {'token_contract': token_contract}) };
    function dex_set_token_as_red_flag(token_contract){ ajax_call('dex_set_token_as_red_flag', {'token_contract': token_contract}) };
    
    function dex_buy_token_by_fiat_amount(token_contract){ 
		const fiat_amount = $(`#dex_buy_token_fiat_amount__input`).val();
        ajax_call('dex_buy_token', {'token_contract': token_contract, 'fiat_amount': fiat_amount})
    };

    function dex_sell_token(token_contract, sell_percentage){ 
        ajax_call('dex_sell_token', {'token_contract': token_contract, 'sell_percentage': sell_percentage})
    };

    function dex_check_balance_token(token_contract){ 
        ajax_call('dex_check_balance_token', {'token_contract': token_contract})
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
