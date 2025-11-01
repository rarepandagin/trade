
import dashboard.views_pages.toolkit as tk
from dashboard.models import models_token, models_adminsettings
from dashboard.modules.dapps.dex.dex_class import Dex
from dashboard.views_pages import transaction_dispatch

def handle_ajax_posts_dex(req, payload):

    admin_settings = tk.get_admin_settings()

    if req == "dex_delete_all_tokens":
        
        models_token.Token.objects.filter(imported=False).delete()


    elif req == "dex_hide_token":
        
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
        token = models_token.Token.objects.get(contract=payload['token_contract'])
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
            if 0 < fiat_amount < 100:
                transaction_dispatch.create_and_actualize_dex_fiat_to_token_transaction(
                        fiat_to_token_amount=fiat_amount,
                        token_contract=token_contract
                    )
            else:
                tk.send_message_to_frontend_dashboard(topic='display_toaster', payload={'message': f'invalid amount', 'color': 'red'})

        else:
            tk.send_message_to_frontend_dashboard(topic='display_toaster', payload={'message': f'you need to switch to DEX account', 'color': 'red'})


    elif req == 'dex_approve_token':
        transaction_dispatch.create_and_actualize_dex_approve_token_transaction(payload['token_contract'])


    elif req == 'dex_sell_token':
        token_contract = payload['token_contract']
        token = models_token.Token.objects.get(contract=token_contract)
        sell_percentage = float(payload['sell_percentage'])
        dex = Dex()

        balance = dex.check_balance_of_token_by_contract_address(token_contract)
        token_amount_to_sell = int(((sell_percentage / 100) * balance))

        transaction_dispatch.create_and_actualize_dex_token_to_fiat_transaction(
            token_to_fiat_amount=token_amount_to_sell,
            token_contract=token_contract
        )



    elif req == 'dex_check_balance_token':
        token_contract = payload['token_contract']
        token = models_token.Token.objects.get(contract=payload['token_contract'])
        
        dex = Dex()

        token.balance = dex.check_balance_of_token_by_contract_address(token_contract)

        quote_fiat_amount = float(payload['quote_fiat_amount'])

        quote = dex.v2_quote(
                token_contract_address=token_contract,
                token_decimals=token.decimals,
                buying_token=True,
                fiat_amount=quote_fiat_amount,
            )

        if quote is None:
            tk.logger.info(f"quote for {token.name} failed.")
        else:
            token.price = quote

        token.save()







