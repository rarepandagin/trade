from django.db import models
from django.db.models.base import transaction

from dashboard.views_pages import toolkit as tk

from dashboard.models import models_adminsettings, models_order
from dashboard.modules.dapps.uniswap.uniswap_class import Uniswap
from dashboard.modules.dapps.sushiswap.sushiswap_class import Sushiswap
from dashboard.modules.dapps.aave.aave_class import Aave
from dashboard.modules.dapps.arbi.arbi_class import Arbi
from dashboard.modules.dapps.dex.dex_class import Dex

from dashboard.models.coins import *


transaction_state_ongoing = "transaction_state_ongoing"
transaction_state_failed = "transaction_state_failed"
transaction_state_successful = "transaction_state_successful"

transaction_states = {
    transaction_state_ongoing : "transaction_state_ongoing",
    transaction_state_failed : "transaction_state_failed",
    transaction_state_successful : "transaction_state_successful",
}

# Uniswap
uniswap_approve = "uniswap_approve"
uniswap_token_to_fiat = "uniswap_token_to_fiat"
uniswap_fiat_to_token = "uniswap_fiat_to_token"
uniswap_wrap_eth = "uniswap_wrap_eth"
uniswap_unwrap_weth = "uniswap_unwrap_weth"
uniswap_transfer_token = "uniswap_transfer_token"


# Sushiswap
sushiswap_token_to_fiat = "sushiswap_token_to_fiat"
sushiswap_fiat_to_token = "sushiswap_fiat_to_token"


# Aave
aave_approve = "aave_approve"
aave_supply = "aave_supply"
aave_withdraw = "aave_withdraw"
aave_borrow = "aave_borrow"
aave_repay = "aave_repay"


# arbi
arbi_balance = "arbi_balance"
arbi_allowance = "arbi_allowance"
arbi_action_2 = "arbi_action_2"
arbi_approve = "arbi_approve"
arbi_deposit = "arbi_deposit"
arbi_withdraw = "arbi_withdraw"
arbi_wrap_eth = "arbi_wrap_eth"
arbi_unwrap_weth = "arbi_unwrap_weth"
arbi_single_swap = "arbi_single_swap"

# dex
dex_quote_token = "dex_quote_token"
dex_approve_token = "dex_approve_token"
dex_fiat_to_token = "dex_fiat_to_token"
dex_token_to_fiat = "dex_token_to_fiat"

transaction_types = {
    uniswap_approve : "uniswap_approve",
    uniswap_token_to_fiat : "uniswap_token_to_fiat",
    uniswap_fiat_to_token : "uniswap_fiat_to_token",
    uniswap_wrap_eth : "uniswap_wrap_eth",
    uniswap_unwrap_weth : "uniswap_unwrap_weth",
    uniswap_transfer_token: "uniswap_transfer_token",

    sushiswap_token_to_fiat : "sushiswap_token_to_fiat",
    sushiswap_fiat_to_token : "sushiswap_fiat_to_token",

    aave_approve : "aave_approve",
    aave_supply : "aave_supply",
    aave_withdraw : "aave_withdraw",
    aave_borrow : "aave_borrow",
    aave_repay : "aave_repay",

    arbi_balance : "arbi_balance",
    arbi_action_2 : "arbi_action_2",
    arbi_approve : "arbi_approve",
    arbi_allowance : "arbi_allowance",
    arbi_deposit : "arbi_deposit",
    arbi_withdraw : "arbi_withdraw",
    arbi_wrap_eth: "arbi_wrap_eth",
    arbi_unwrap_weth: "arbi_unwrap_weth",
    arbi_single_swap: "arbi_single_swap",

    dex_quote_token: "dex_quote_token",
    dex_approve_token: "dex_approve_token",
    dex_fiat_to_token: "dex_fiat_to_token",
    dex_token_to_fiat: "dex_token_to_fiat",
}


class Transaction(models.Model):

    id = models.BigAutoField(primary_key=True)

    # initial setup

    transaction_type    = models.CharField(choices=transaction_types,   default=uniswap_token_to_fiat)
    state               = models.CharField(choices=transaction_states,  default=transaction_state_ongoing)
    
    order = models.ForeignKey(models_order.Order, on_delete=models.SET_NULL, null=True, blank=True)

    coin = models.CharField(choices=coins, default=weth)

    # fiat_to_token
    fiat_amount_spent        = models.FloatField(default=0)
    token_amount_received     = models.FloatField(default=0)
    
    # token_to_fiat
    token_amount_spent        = models.FloatField(default=0)
    fiat_amount_received     = models.FloatField(default=0)
    
    token_nominal_price       = models.FloatField(default=0) # from quote
    token_effective_price     = models.FloatField(default=0) # actually what happened
    slippage                 = models.FloatField(default=0)

    hash                    = models.TextField(default="", null=True, blank=True)
    fee                     = models.FloatField(default=0)

    address_to_transfer_to  = models.TextField(default="", null=True, blank=True)
    
    # case specific fields
    fiat_loan_amount        = models.FloatField(default=0)
    dex_token_contract      = models.TextField(default="", null=True, blank=True)

    # auto
    uuid = models.TextField(default="", blank=True, null=True)
    name = models.TextField(default="", blank=True, null=True)
    epoch_created = models.BigIntegerField(default=0)
    epoch_updated = models.BigIntegerField(default=0)





    def save(self, *args, **kwargs):
        if self.uuid == '':
            self.uuid = tk.get_new_uuid()
            self.epoch_created = tk.get_epoch_now()
            self.name = tk.get_new_random_name()

        else:
            self.epoch_updated = tk.get_epoch_now()


        self.token_nominal_price                  = round(self.token_nominal_price, 2)
        self.token_effective_price                = round(self.token_effective_price, 2)

        super(Transaction, self).save(*args, **kwargs)


    def actualize(self):

        tk.send_message_to_frontend_dashboard(topic='display_toaster', payload={'message': f'starting to actualize {self.transaction_type} tx ({self.name})', 'color': 'green'})



        admin_settings = tk.get_admin_settings()

        gas_price_is_acceptable = admin_settings.gas['gas_basic_price'] < admin_settings.max_sane_gas_price
        gas_price_is_recent = tk.get_epoch_now() - admin_settings.gas_update_epoch < admin_settings.gas_update_epoch_max_allowed_delay_seconds

        if not (gas_price_is_acceptable and gas_price_is_recent):
        # if False:
            self.state = transaction_state_failed
            tk.send_message_to_frontend_dashboard(topic='display_toaster', payload={'message': f'gas price is too expensive or outdated. aborting the tx.', 'color': 'red'})

        else:


            if 'uniswap_' in str(self.transaction_type):
        
                uniswap = Uniswap()

                # relevant added slippage multiplier is calculated by quoting before executing the swap 

                if self.transaction_type == uniswap_approve:
                    if uniswap.approve_spenders():
                        self.state = transaction_state_successful
                    else:
                        self.state = transaction_state_failed


                if self.transaction_type == uniswap_fiat_to_token:

                    tk.update_admin_settings("gas_speed", models_adminsettings.FastGasPrice)


                    uniswap.create_new_quote_and_save_to_db(fiat_to_coin=True, fiat_amount_in=self.fiat_amount_spent)

                    got_token, token_bought, tx_hash, token_price, tx_fee = uniswap.fiat_to_token(
                            fiat_amount=self.fiat_amount_spent,
                            token=self.coin,
                            tries=admin_settings.tx_tries,
                            transaction_object=self,
                        )


                    if got_token:
                        expected_token_based_on_nominal_price = self.fiat_amount_spent / token_price
                        slippage = (expected_token_based_on_nominal_price - token_bought) / expected_token_based_on_nominal_price
                        slippage = round(slippage, 6)

                        self.token_amount_received = token_bought
                        # self.hash = tx_hash
                        self.token_nominal_price = token_price
                        self.token_effective_price = self.fiat_amount_spent / self.token_amount_received
                        self.slippage = slippage
                        self.state = transaction_state_successful
                        self.fee = round(tx_fee, 2)

                    else:
                        self.state = transaction_state_failed


                elif self.transaction_type == uniswap_token_to_fiat:
                    tk.update_admin_settings("gas_speed", models_adminsettings.FastGasPrice)

                    # uniswap.create_new_quote_and_save_to_db(fiat_to_coin=False, coin_amount_in=self.token_amount_spent)

                    got_fiat, fiat_bought, tx_hash, token_price, tx_fee = uniswap.token_to_fiat(
                        token_amount=self.token_amount_spent,
                        token=self.coin,
                        tries=admin_settings.tx_tries,
                        transaction_object=self,
                    )


                    if got_fiat:
                        expected_fiat_base_on_nominal_price = self.token_amount_spent * token_price
                        slippage = (expected_fiat_base_on_nominal_price-fiat_bought)/expected_fiat_base_on_nominal_price
                        slippage = round(slippage, 6)

                        self.fiat_amount_received = fiat_bought
                        # self.hash = tx_hash
                        self.token_nominal_price = token_price
                        self.token_effective_price = self.fiat_amount_received / self.token_amount_spent
                        self.slippage = slippage
                        self.state = transaction_state_successful
                        self.fee = round(tx_fee, 2)

                    else:
                        self.state = transaction_state_failed
        

                elif self.transaction_type == uniswap_wrap_eth:
                    if uniswap.wrap_eth(eth_amount=self.token_amount_spent):
                        self.state = transaction_state_successful
                    else:
                        self.state = transaction_state_failed


                elif self.transaction_type == uniswap_unwrap_weth:
                    if uniswap.unwrap_weth(eth_amount=self.token_amount_spent):
                        self.state = transaction_state_successful
                    else:
                        self.state = transaction_state_failed

                elif self.transaction_type == uniswap_transfer_token:
                    successful, _, tx_hash, tx_fee_in_eth = uniswap.send_token(
                        token=self.coin,
                        amount=self.token_amount_spent,
                        receiver_address=self.address_to_transfer_to,
                        transaction_object=self,
                    )

                    self.state = transaction_state_successful if successful else transaction_state_failed



            elif 'sushiswap_' in str(self.transaction_type):
                sushiswap = Sushiswap()

                if self.transaction_type == sushiswap_fiat_to_token:
                    got_token, token_bought, tx_hash, token_price, tx_fee = sushiswap.fiat_to_token(
                            fiat_amount=self.fiat_amount_spent,
                            token=self.coin,
                            tries=admin_settings.tx_tries,
                            transaction_object=self,
                        )


                if self.transaction_type == sushiswap_token_to_fiat:
                    pass



            elif 'aave_' in str(self.transaction_type):
                aave = Aave()

                tk.update_admin_settings("gas_speed", models_adminsettings.SafeGasPrice)

                

                def process_aave_transaction_receipt(receipt_dict):
                    
                    self.hash = receipt_dict['tx_hash'] 
                    tx_fee = receipt_dict['tx_fee_in_eth'] * admin_settings.prices['weth'] 
                    self.fee = round(tx_fee, 2)

                    if receipt_dict['successful']:
                        self.state = transaction_state_successful
                    else:
                        self.state = transaction_state_failed


                if self.transaction_type == aave_approve:
                    if aave.approve_spenders():
                        self.state = transaction_state_successful
                    else:
                        self.state = transaction_state_failed

                elif self.transaction_type == aave_supply:
                    ret = aave.supply(aave.weth, self.token_amount_spent)
                    process_aave_transaction_receipt(ret)

                elif self.transaction_type == aave_withdraw:
                    ret = aave.withdraw(aave.weth, self.token_amount_spent)
                    process_aave_transaction_receipt(ret)

                elif self.transaction_type == aave_borrow:
                    if admin_settings.borrow_from_aave:
                        ret = aave.borrow(aave.weth, self.token_amount_spent)
                    else:
                        ret =  {
                                    'successful': True,
                                    'tx_hash': "no hash. aave tx was skipped",
                                    'tx_fee_in_eth': 0,
                                    'logs_results': [],
                                }
                    process_aave_transaction_receipt(ret)

                elif self.transaction_type == aave_repay:
                    if admin_settings.borrow_from_aave:
                        ret = aave.repay(aave.weth, self.token_amount_spent)
                    else:
                        ret =  {
                                    'successful': True,
                                    'tx_hash': "no hash. aave tx was skipped",
                                    'tx_fee_in_eth': 0,
                                    'logs_results': [],
                                }
                    process_aave_transaction_receipt(ret)


            elif 'arbi_' in str(self.transaction_type):
                arbi = Arbi()

                
                arbi.token_one = arbi.usdc
                arbi.token_two = arbi.dai


                if self.transaction_type == arbi_balance:
                    arbi.get_balance()

                elif self.transaction_type == arbi_wrap_eth:
                    arbi.wrap_eth(self.token_amount_spent)

                elif self.transaction_type == arbi_unwrap_weth:
                    arbi.unwrap_weth(self.token_amount_spent)


                elif self.transaction_type == arbi_allowance:
                    arbi.get_allowance()


                elif self.transaction_type == arbi_deposit:
                    arbi.deposit()


                elif self.transaction_type == arbi_withdraw:
                    arbi.withdraw()


                elif self.transaction_type == arbi_action_2:
                    ret = arbi.perform_flash_loan(token_one=arbi.usdc, token_two=arbi.dai, token_one_amount=self.fiat_loan_amount)
                    # ret = arbi.hello_action()


                elif self.transaction_type == arbi_approve:
                    if arbi.approve_spenders():
                        self.state = transaction_state_successful
                    else:
                        self.state = transaction_state_failed



                elif self.transaction_type == arbi_single_swap:
                    ret = arbi.perform_single_swap()

            elif 'dex_' in str(self.transaction_type):

                dex = Dex()

                tk.update_admin_settings('active_account', models_adminsettings.account_dex)


                if self.transaction_type == dex_quote_token:
                    from dashboard.models import models_token
                    token = models_token.Token.objects.get(contract=self.dex_token_contract)

                    quote = dex.v2_quote(
                            token_contract_address=self.dex_token_contract,
                            token_decimals=token.decimals,
                            buying_token=True,
                            fiat_amount=self.fiat_amount_spent,
                        )

                    if quote is None:
                        self.state = transaction_state_failed
                    else:

                        token.price = quote
                        self.state = transaction_state_successful
                        token.save()

                elif self.transaction_type == dex_approve_token:

                    successful = dex.approve_spenders(token_contract_address=self.dex_token_contract)

                    from dashboard.models import models_token
                    token = models_token.Token.objects.get(contract=self.dex_token_contract)
                    token.approved = successful
                    token.save()


                elif self.transaction_type == dex_token_to_fiat:

                    from dashboard.models import models_token
                    
                    token = models_token.Token.objects.get(contract=self.dex_token_contract)

                    successful, weth_received, tx_fee = dex.token_to_weth(
                        token_contract_address=self.dex_token_contract,
                        token_decimals=token.decimals,
                        token_amount_to_sell=self.token_amount_spent,
                        tries=admin_settings.tx_tries,
                        transaction_object=self,
                    )
                    if successful:
                        self.fiat_amount_received = weth_received
                        self.state = transaction_state_successful
                        self.fee = round(tx_fee, 2)

                    else:
                        self.state = transaction_state_failed


                elif self.transaction_type == dex_fiat_to_token:
                    
                    if 0 < self.fiat_amount_spent < 50:

                        from dashboard.models import models_token
                        token = models_token.Token.objects.get(contract=self.dex_token_contract)

                        successful, token_bought, tx_hash, tx_fee = dex.fiat_to_token(
                            token_contract_address=self.dex_token_contract,
                            token_decimals=token.decimals,
                            fiat_amount=self.fiat_amount_spent,
                            tries=admin_settings.tx_tries,
                            transaction_object=self,
                        )

                        if successful:
                            self.token_amount_received = token_bought
                            self.hash = tx_hash
                            self.state = transaction_state_successful
                            self.fee = round(tx_fee, 2)

                        else:
                            self.state = transaction_state_failed



        if self.state == transaction_state_successful:
            tk.send_message_to_frontend_dashboard(topic='display_toaster', payload={'message': f'tx {self.name} ({self.transaction_type}) was successful', 'color': 'green'})

        elif self.state == transaction_state_failed:
            tk.send_message_to_frontend_dashboard(topic='display_toaster', payload={'message': f'tx {self.name} ({self.transaction_type}) failed', 'color': 'red'})