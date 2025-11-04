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

		

		locked_liquidity_html += `<button type="button" class="btn btn-secondary btn-sm disable_while_busy m-1" style="height: 30px;" onclick="copy_to_clipboard('${this.contract}')">copy contract</button>`


		if (this.go_plus_locked_lp_ratio>0){
			locked_liquidity_html += `<br><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1190 1280" fill="currentColor" width="10px" height="10px" style="margin-left: 5px;"><path d="M561 80.1c-109.6 8.8-192.4 62.6-237.5 154.4-8 16.2-15.5 34.7-15.5 38 0 .8-.4 1.5-.8 1.5s-.8.8-.9 1.7c-.1 1.9-.6 3.8-1.6 6.3-1.7 4.7-7.8 28.7-9.1 36-.3 1.9-.8 4.6-1.1 5.9-.2 1.4-.7 4.7-1 7.4-.3 2.8-.8 5.3-1 5.6-.8 1.3-2.4 18.9-2.8 31.3-.1 2.7-.5 4.8-1 4.8-.4 0-.3.9.3 2 .8 1.4.8 2 0 2-.7 0-.8.6-.1 1.9.6 1 .8 2.1.5 2.4-.3.3-.5 39.2-.4 86.5l.1 86-2.6 2c-1.4 1.1-6.9 3-12.3 4.3-15.9 3.6-26.6 7.4-36.4 12.8-10.9 6-14.9 9.1-24 18.3-20.6 20.8-33.4 56-35.3 96.8-.5 9.9-.4 302.2.1 312.5.8 17.5 2.8 31.9 4.6 34.3.7.8.7 1.2-.1 1.2-.7 0-.9.5-.4 1.3.4.6.8 1.6.9 2.2.1.5 1.1 3.4 2.3 6.2 1.1 2.9 1.7 5.3 1.3 5.3-.4 0-.2.4.3.8 1 .7 3.7 6.1 3.7 7.2 0 .3.6 1.2 1.4 2.1.8.9 1.2 1.8.9 2.1-.3.3.6 1.7 2 3.2 1.3 1.4 2.5 2.9 2.5 3.1 0 1.4 8.4 11.7 12.2 15 2.4 2.1 3.4 3.2 2.3 2.4-1.8-1.3-1.9-1.3-.6.3.7 1 1.7 1.8 2.2 1.8.5 0 1.7.8 2.7 1.7 3.9 3.7 6.7 5.7 12.1 8.6 17.5 9.4 26.7 12.1 52.1 15.3 11.1 1.3 46.1 1.5 312.1 1.4 310.6 0 312.3 0 331.4-3.9 22.1-4.5 39.7-13.4 53.1-27 16.1-16.2 23.8-34.2 26.9-62.6 1.2-10.7 1.5-40.7 1.5-169.6 0-86.2-.2-157.3-.4-158-.3-.8-.7-6.3-1-12.2-.4-6-.8-11.2-1-11.6-.3-.4-.7-2.7-1-5.1-1.7-14.3-7.6-34.2-13.7-46.3-3-5.7-10.7-17.6-13.8-21.1-6.2-6.9-15.9-16-17.4-16.4-1.3-.3-3.7-3-3.8-4.4 0-.7-.4-.4-.8.7-.8 1.9-.8 1.9-1.5-.3-.5-1.4-1.3-2.1-2.1-1.8-.8.3-1.9-.2-2.5-1-.7-.8-1.9-1.4-2.6-1.4-.8 0-1.4-.5-1.4-1 0-.6-.7-1-1.5-1s-1.5-.5-1.5-1c0-.6-.9-1-2-1s-2-.5-2-1.1c0-.5-.4-.7-1-.4-.5.3-1 .1-1-.5s-.4-.8-1-.5c-.5.3-1 .2-1-.4 0-.5-.8-.8-1.7-.6-1 .1-3-.4-4.5-1.1-1.5-.8-3.1-1.3-3.5-1.3-.4.1-1.6-.1-2.5-.4-4.6-1.8-5.4-2-6.9-2.3-.9-.2-2.7-.8-4-1.3-1.3-.5-2.7-.8-3-.7-.4 0-1.7-.8-3-1.9-1.4-1.3-2-1.4-1.5-.5.4.8-.4.2-1.8-1.3l-2.6-2.8v-84.7c-.1-46.6-.3-88.3-.5-92.7-.7-11.7-1.4-20.6-1.9-24-.3-2.4-2.6-16.9-4-25.5-2.1-12.5-3-17-3.6-17-.4 0-.6-1-.5-2.3.1-1.2-.1-2.7-.5-3.2-.5-.6-1.1-2.4-1.3-4-.9-4.6-1.4-6.8-2.5-9.6-.6-1.5-.8-2.9-.6-3.2.3-.3-.2-2.2-1-4.2-.9-2.1-1.6-4.7-1.6-5.9 0-1.6-.2-1.8-.9-.7-.7 1-1.1.1-1.6-3.2-.4-2.6-1.2-4.7-1.7-4.7-.6 0-.8-.9-.5-2 .3-1.1.1-2-.4-2s-.9-.7-.9-1.5-.4-1.5-1-1.5c-.5 0-.6-.7-.3-1.7.5-1.1.3-1.4-.6-.8-1 .6-1.1.2-.6-1.5.5-1.7.4-2.1-.5-1.5-.8.5-1.1.4-.6-.3.7-1.1-2.8-9.3-9.6-22.7-2.2-4.4-5.5-10.7-7.1-14-1.7-3.3-3.4-6.2-3.8-6.5-.3-.3-1.6-2.5-2.9-4.9-1.2-2.4-2.6-4.9-3.1-5.5-3-3.6-8.4-11.3-10.5-14.9-1.3-2.3-2.4-3.8-2.4-3.4 0 .4-.6.2-1.4-.5-.8-.7-1.2-1.6-.9-2 .2-.4-.7-1.9-2.1-3.3-1.5-1.4-2.6-3.1-2.6-3.7 0-.6-.3-.8-.7-.5-.3.4-1.3-.2-2-1.3-.8-1.1-1.9-1.8-2.4-1.5-.5.4-.9-.2-.9-1.2 0-1.1-2-3.9-4.5-6.3-2.4-2.4-4.2-4.7-3.9-5.2.3-.4-.4-.8-1.5-.8s-2.2-.9-2.6-2c-.3-1.1-1.3-2-2.1-2s-1.4-.7-1.4-1.5-.7-1.5-1.6-1.5c-.8 0-1.2-.5-.9-1 .3-.6-.1-1-.9-1-.9 0-1.6-.5-1.6-1.1 0-.5-.3-.8-.7-.6-.5.3-1.4-.1-2.1-.9-.7-.8-.9-1.4-.5-1.4.4-.1-.4-.8-1.9-1.6-1.6-.8-2.8-1.9-2.8-2.4 0-.6-.7-1-1.5-1s-1.5-.5-1.5-1c0-.6-.5-1-1-1-.6 0-2.1-1.1-3.4-2.5-1.3-1.4-2.6-2.5-3-2.5-.7 0-6.7-4.1-7.6-5.1-.3-.3-1.9-1.3-3.7-2.2-1.7-.9-3.7-2.2-4.5-2.9-1.8-1.7-5.9-4.2-14.3-8.5-3.8-1.9-7.3-4-7.6-4.5-.3-.5-.9-.9-1.2-.9-.4 0-2.6-.8-4.9-1.8-37.4-15.8-66.5-22.9-107.2-26.1-15-1.2-50.4-1.1-65.6.1zm47.5 121.4c10.3 1 14 1.5 24 3.1 9 1.5 28.3 6.7 31.4 8.5 1.7.9 7.4 3.1 7.9 3 1-.4 27.3 14.8 29.2 17 .3.3 2.3 1.8 4.4 3.5 2.2 1.6 4.9 3.8 6 4.9 1.2 1.1 3.5 3.1 5.1 4.3 1.7 1.3 2.3 2.1 1.5 1.7-.8-.4-.1.6 1.6 2.2 2.7 2.4 9.8 10.7 15.7 18.4 1 1.3 2.7 4 3.8 5.9 1.1 1.9 2.8 4.8 3.9 6.5 1.9 3 7.3 12.6 7.5 13.5.1.3 1 2.3 2 4.5s1.8 4.3 1.7 4.7c-.1.5.2.8.6.8.5 0 .9.6 1 1.2.2 2.9 2.9 8.8 3.7 8.1.4-.5.5-.3.1.4s.7 5 2.3 9.7c1.6 4.6 2.7 8.7 2.4 9-.3.3 0 1.2.7 2.1.7.9 1 1.8.7 2.2-.4.3-.2 1.2.4 2 .9 1 .8 1.3-.2 1.3-.9.1-.8.5.5 1.5 1.1.8 1.5 1.5.8 1.5-.8 0-.9.7-.1 2.7.6 1.6 1.2 3.7 1.4 4.8.8 4.9 2.7 20.3 2.9 23 0 1.6.5 3.3 1.1 3.7.7.5.6.8 0 .8s-1.1.9-1.1 2 .4 2 .9 2 .4.6-.2 1.4c-.9 1.1-.9 1.5.1 2s1 .7.1 1.2c-1.9.8-1.6 2.4.5 2.4 1 0 1.3.3.6.8-1.6 1-1.8 22.2-.3 22.2.8 0 .9.4 0 1.3-.8 1-1.2 21.5-1.3 70.7l-.3 69.4-3.4 2c-3.4 2-5.6 2-171.7 2.4-121.6.3-168.3.1-168.8-.7-.4-.6-2.2-1.1-4-1.1-6.9 0-6.5 5.9-6.6-90.5-.1-47.9-.1-87.2 0-87.5.1-.3.3-3.2.5-6.5.4-6.5 1-11.7 2.6-21 .6-3.3 1.2-7.1 1.3-8.5.2-1.4.6-3.2 1-4.1.4-.9.8-2.7 1-4.1.1-1.3.5-2.8.8-3.3.3-.6.9-2.8 1.3-5 .8-4.2 4.7-15.9 7.1-21.2.8-1.7 1.4-3.4 1.4-3.9 0-3.3 18.8-35.6 24.7-42.4 3.6-4.2 19.7-20 23.9-23.5 11-9.3 39.8-24 50.7-25.9.7-.1 2.8-.7 4.7-1.4 5.8-1.9 27.3-5.2 38.2-5.8 5.7-.4 10.4-.7 10.5-.8.4-.3 15.6.3 21.8.9z"></path></svg>`
			locked_liquidity_html += `LP: ${this.go_plus_lp_total_supply.toFixed(4)} (ratio: ${this.go_plus_locked_lp_ratio.toFixed(2)})</p>`
			
		} else {
			locked_liquidity_html += `<p class="text-danger"><strong>LP tokens are not locked</strong></p>`
		}

		if(this.uncx_pool_lock_ratio > 0) {
			let uncx_lock_until = this.uncx_epoch_end_lock - Math.floor(Date.now() / 1000)
			if (uncx_lock_until > 0){
				locked_liquidity_html += `<a  target="_blank"  href="https://app.uncx.network/lockers/univ2/chain/1/address/${this.pair_address}/lock/0">
				
				<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24.9 24.9" focusable="false" class="chakra-icon custom-v5w1at"><defs><linearGradient id="a" x1="12.45" x2="12.45" y1="24.9" y2="0" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#00c68d"></stop><stop offset="1" stop-color="#00f847"></stop></linearGradient></defs><path d="M24.89 11.92c-.05-1.22-.28-2.4-.67-3.51-.03-.11-.08-.22-.12-.31C22.33 3.37 17.78 0 12.45 0 5.59 0 0 5.59 0 12.45S5.59 24.9 12.45 24.9c.54 0 1.08-.03 1.6-.11h.03c6-.79 10.65-5.86 10.8-12.03.01-.1.01-.21.01-.31v-.27c0-.09 0-.17-.01-.26Zm-22.72.53c0-5.67 4.61-10.28 10.28-10.28 3.18 0 6.03 1.45 7.94 3.72-.7-.14-1.47-.11-2.22.27L18 4.22a.177.177 0 0 0-.28-.13l-2.23 1.66-.6-1.07a.172.172 0 0 0-.31 0l-.75 1.36c-.79.26-1.52.69-2.13 1.35L5.65 5.73c-.18-.08-.31.17-.16.28 1.95 1.41 4.74 3.09 4.77 3.12 0 0-4.04 6.35-4.04 6.37-.62 1-.28 1.84.76 2.38.58.29 1.25.41 1.89.35.91-.1 2.72-.42 5.48-1.34.28.48.44 1.12.44 1.8 0 1.29-.57 2.77-2.02 3.77-.13.1-.28.18-.43.28-5.62-.06-10.17-4.66-10.17-10.28Zm10.77.25s-1.02.91-2.35.27l2.57-2.31s.81 1.1-.22 2.04Z" style="fill: url(&quot;#a&quot;); stroke-width: 0;"></path></svg>
				${this.uncx_pool_lock_ratio.toFixed(2)}, until ${readable_elapsed_delta_epochs(uncx_lock_until)}
				</a>`
			}

		}

		let html = `
			<a href ="https://www.dextools.io/app/en/ether/pair-explorer/${this.contract}" target="_blank" >${this.name}</a>
			<a href ="https://dexscreener.com/ethereum/${this.contract}" target="_blank" >					<img width="20" src="https://imgs.search.brave.com/X2FR-rkSBkwMZFSrVMoz9VWmE-HMF9FS3I5JSqPCZ7M/rs:fit:32:32:1:0/g:ce/aHR0cDovL2Zhdmlj/b25zLnNlYXJjaC5i/cmF2ZS5jb20vaWNv/bnMvYmFlNGRlNGI2/ZjJjMjFmMWZlY2Ux/ZDA0NWQ3OGUyMjNi/MDM3NmE3ZmQyYzFl/YzUwODE5MzA0MzU1/NTM3MTQ3ZC9kZXhz/Y3JlZW5lci5jb20v" /></a>
			<a href ="https://www.dextools.io/app/en/ether/pair-explorer/${this.contract}" target="_blank" ><img width="20" src="https://imgs.search.brave.com/z1-B0wYNTgZ57OcyXh6qPMKNA0MIEgciLhw3R1jJ3u0/rs:fit:32:32:1:0/g:ce/aHR0cDovL2Zhdmlj/b25zLnNlYXJjaC5i/cmF2ZS5jb20vaWNv/bnMvMDQ5YWRjZDMx/MTQ2Nzk4NTY4ZjJm/ZWZmZDI4NTExY2Nj/MmM3MGQzYWU0ZjEw/ZDZjNjUyYzMyNDIz/OTY0YzUwOS9kZXh0/b29scy5pby8" /></a>
			<a href ="https://tokensniffer.com/bubble/v2/eth/${this.contract}" target="_blank" >			<img width="20" src="https://cdn.prod.website-files.com/5dc2e688a258f6237d614aa3/65788d7aa6d10a3395a17f62_Sniffer%20Pack%20Pro.svg" /></a>
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
			html+=`<span class="badge rounded-pill bg-${color} fs-6">${x}</span><br>`
		})

		
		html += `
			<a href="https://etherscan.io/address/${this.pair_address}" target="_blank">
				pool weth: ${(this.weth_pair_reserves/Math.pow(10, 18)).toFixed(2)}
			</a>
			<br>
			price / weth: <span class="text-info">${this.price_per_weth}</span>
		`

		return html;
	}


	get_investigation_html(){

		let status_html = ``

		if (this.investigated){

			if (this.keep_investigating){
				status_html += `<p>Being re-investigated...</p>`
			}
			
			if (this.investigation_pass){
				status_html += `<p class="text-success elementToFade fs-4">PASS</p>`
			}

			if (this.investigation_safe){
				status_html += `<p class="text-warning elementToFade fs-4">SAFE</p>`
			}

			if (this.investigation_red_flag){
				status_html += `<p class="text-danger">Red flag</p>`
			}

		} else {
			status_html += `<p class="text-warning">not investigated yet</p>`
		}

		return status_html;
		
	}

	get_lp_html(){
		let sub_html
		if ((this.go_plus_locked_lp_ratio>0) && (this.uncx_pool_lock_ratio > 0)){
			sub_html = `success`
		} else if ((this.go_plus_locked_lp_ratio>0) || (this.uncx_pool_lock_ratio > 0)){
			sub_html = `warning`
		} else {
			sub_html = `danger`
		}
		
		let html = `
			<p class="text-${sub_html}">${this.go_plus_dex_liquidity}</p>
		`

		return html
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

		return social_html

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
	
	payload.admin_settings.tokens.sort((a, b) => b.pair_creation_epoch - a.pair_creation_epoch);
	
	// payload.admin_settings.tokens = payload.admin_settings.tokens.filter(x=>x.liquidity > 0)

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
			<th>Dex Liquidity</th>
			<th>Age</th>
			<th>Security</th>
			
			
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
				<td>${token.get_lp_html()}</td>
				<td>${token.get_age_html()}</td>
				<td>${token.get_security_html()}</td>
				
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

	payload.admin_settings.tokens.sort((a, b) => b.pair_creation_epoch - a.pair_creation_epoch);

	let tokens = []

	payload.admin_settings.tokens.forEach(x=>tokens.push(new Token(x)))
	
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
						${token.get_pair_html()}<br>
						${token.get_lp_html()}<br>
						${token.get_investigation_html()}<br>
						${token.get_security_html()}<br>

					</td>

					<td>
						<div class="vstack  gap-2">
							<p>Balance: ${token.balance}</p>

							<p>Price: ${token.price} $<br>
							Value: ${(token.price * token.balance).toFixed(2)} $</p><br>
							<button type="button" onclick="dex_check_balance_token('${token.contract}');" class="btn btn-primary btn-sm m-1">check balance</button>

							</div>
					</td>

					
					<td>
						<div class="d-flex justify-content-start  gap-2">

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





	
    function dex_delete_all_tokens(){ ajax_call('dex_delete_all_tokens', {}) };
    function dex_delete_all_tokens(){ ajax_call('dex_delete_all_tokens', {}) };
    function dex_hide_token(token_contract){ ajax_call('dex_hide_token', {'token_contract': token_contract}) };
    function dex_toggle_token_on_chart(token_contract){ ajax_call('dex_toggle_token_on_chart', {'token_contract': token_contract}) };
    function dex_import_token(token_contract){ ajax_call('dex_import_token', {'token_contract': token_contract}) };
    function dex_remove_import_token(token_contract){ ajax_call('dex_remove_import_token', {'token_contract': token_contract}) };
    
    function dex_buy_token(token_contract){ 
		const fiat_amount = $(`#dex_fiat_amount_buy__input`).val();
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
