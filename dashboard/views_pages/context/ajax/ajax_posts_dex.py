
from eth_utils import address
import dashboard.views_pages.toolkit as tk
from dashboard.models import models_token, models_adminsettings
from dashboard.modules.dapps.dex.dex_class import Dex

def handle_ajax_posts_dex(req, payload):

    admin_settings = tk.get_admin_settings()

    if req == "dex_hide_token":
        
        token = models_token.Token.objects.get(contract=payload['token_contract'])
        token.show = False
        token.save()


    elif req == "dex_toggle_token_on_chart":
        
        token = models_token.Token.objects.get(contract=payload['token_contract'])
        token.show_on_chart = not token.show_on_chart
        token.save()

    elif req == "dex_remove_import_token":
        token = models_token.Token.objects.get(contract=payload['token_contract'])
        token.imported = False
        token.save()

    elif req == "dex_import_token":
        

        dex = Dex()

        token = models_token.Token.objects.get(contract=payload['token_contract'])

        token_contract = token.contract

        quote = dex.v2_quote(
            token_contract_address=token_contract,
            buying_token=True,
            fiat_amount=1000,
        )

        if quote is not None:
            token.price = quote
            token.imported = True
            token.save()



    elif req == 'dex_add_token_manually':
        new_token_name = payload['new_token_name']
        new_token_address = payload['new_token_address']
        new_token_contract = payload['new_token_contract']

        if not models_token.Token.objects.filter(contract=new_token_contract).exists():
            new_token = models_token.Token(
                name=new_token_name,
                address=new_token_address,
                contract=new_token_contract,
            )
            new_token.save()


    elif req == 'dex_buy_token':

        if admin_settings.active_account == models_adminsettings.account_dex:

            token_contract = payload['token_contract']
            fiat_amount = float(payload['fiat_amount'])

            if not 0 < fiat_amount < 50:
                dex = Dex()

                admin_settings = tk.get_admin_settings()

                # dex.fiat_to_token(
                #         token_contract_address=token_contract,
                #         fiat_amount=fiat_amount,
                #         tries=admin_settings.tx_tries
                #     )
            else:
                tk.send_message_to_frontend_dashboard(topic='display_toaster', payload={'message': f'invalid fiat amount', 'color': 'red'})

        else:
            tk.send_message_to_frontend_dashboard(topic='display_toaster', payload={'message': f'you need to switch to DEX account', 'color': 'red'})


    elif req == 'dex_approve_token':
        token_contract = payload['token_contract']
        dex = Dex()
        token = models_token.Token.objects.get(contract=payload['token_contract'])
        token.approved = dex.approve_spenders(token_contract_address=token_contract)
        token.save()


    elif req == 'dex_sell_token':
        token_contract = payload['token_contract']
        sell_percentage = float(payload['sell_percentage'])
        dex = Dex()

        balance = dex.check_balance_of_token_by_contract_address(token_contract)
        token_amount_to_sell = (sell_percentage/ 100) * balance

        dex.token_to_weth(
                token_contract_address=token_contract,
                token_amount_to_sell=token_amount_to_sell,
                tries=admin_settings.tx_tries
            )

    elif req == 'dex_check_balance_token':
        token_contract = payload['token_contract']
        token = models_token.Token.objects.get(contract=payload['token_contract'])
        
        dex = Dex()

        token.balance = dex.check_balance_of_token_by_contract_address(token_contract)


        quote_fiat_amount = float(payload['quote_fiat_amount'])

        quote = dex.v2_quote(
            token_contract_address=token_contract,
            buying_token=True,
            fiat_amount=quote_fiat_amount,
        )


        if quote is not None:

            token.price = quote

        token.save()







    else:


        tk.update_admin_settings("command_function", req)
        tk.update_admin_settings("command_arguments", payload)

