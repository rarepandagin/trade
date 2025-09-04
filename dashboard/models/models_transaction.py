from django.db import models

from dashboard.views_pages import toolkit as tk

from dashboard.models import models_position
from dashboard.modules.uniswap.v3_class import Uniswap

from dashboard.models.coins import *


transaction_state_ongoing = "transaction_state_ongoing"
transaction_state_failed = "transaction_state_failed"
transaction_state_succesful = "transaction_state_succesful"

transaction_states = {
    transaction_state_ongoing : "transaction_state_ongoing",
    transaction_state_failed : "transaction_state_failed",
    transaction_state_succesful : "transaction_state_succesful",
}

token_to_fiat = "token_to_fiat"
fiat_to_token = "fiat_to_token"

transaction_types = {
    token_to_fiat: "token_to_fiat",
    fiat_to_token: "fiat_to_token",
}



class Transaction(models.Model):

    id = models.BigAutoField(primary_key=True)

    # initial setup

    transaction_type    = models.CharField(choices=transaction_types,   default=token_to_fiat)
    state               = models.CharField(choices=transaction_states,  default=transaction_state_ongoing)
    uniswap_version     = models.TextField(default="", blank=True, null=True)
    
    position = models.ForeignKey(models_position.Position, on_delete=models.SET_NULL, null=True, blank=True)

    coin = models.CharField(choices=coins, default=weth)

    # fiat_to_token
    fiat_amount_spent        = models.FloatField(default=0)
    token_amount_recieved     = models.FloatField(default=0)
    
    # token_to_fiat
    token_amount_spent        = models.FloatField(default=0)
    fiat_amount_recieved     = models.FloatField(default=0)
    
    token_nominal_price       = models.FloatField(default=0) # from quote
    token_effective_price     = models.FloatField(default=0) # actually what happened
    slipage                 = models.FloatField(default=0)

    hash                    = models.TextField(default="", null=True, blank=True)
    fee                     = models.FloatField(default=0)


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

        # before actualizing any transaction, we need to make sure that the gas price is lower than a resonable amount
        admin_settings = tk.get_admin_settings()
        if admin_settings.gas['gas_basic_price'] > admin_settings.max_sane_gas_price:
            self.state = transaction_state_failed

        else:
        
            uniswap = Uniswap()

            # relevant added slipage multiplier is calculated by quoting before executing the swap 

            if self.transaction_type == fiat_to_token:

                uniswap.create_new_quote_and_save_to_db(fiat_to_coin=True, fiat_amount_in=self.fiat_amount_spent)

                got_token, token_bought, tx_hash, token_price, tx_fee, version = uniswap.fiat_to_token(
                        fiat_amount=self.fiat_amount_spent,
                        token=self.coin,
                        tries=1
                    )


                if got_token:
                    expected_token_based_on_nominal_price = self.fiat_amount_spent / token_price
                    slipage = (expected_token_based_on_nominal_price - token_bought) / expected_token_based_on_nominal_price
                    slipage = round(slipage, 6)

                    self.token_amount_recieved = token_bought
                    self.hash = tx_hash
                    self.uniswap_version = version
                    self.token_nominal_price = token_price
                    self.token_effective_price = self.fiat_amount_spent / self.token_amount_recieved
                    self.slipage = slipage
                    self.state = transaction_state_succesful
                    self.fee = round(tx_fee, 2)

                else:
                    self.state = transaction_state_failed


            elif self.transaction_type == token_to_fiat:

                uniswap.create_new_quote_and_save_to_db(fiat_to_coin=False, coin_amount_in=self.token_amount_spent)

                got_fiat, fiat_bought, tx_hash, token_price, tx_fee, version = uniswap.token_to_fiat(
                    token_amount=self.token_amount_spent,
                    token=self.coin,
                    tries=1
                )


                if got_fiat:
                    expected_fiat_base_on_nominal_price = self.token_amount_spent * token_price
                    slipage = (expected_fiat_base_on_nominal_price-fiat_bought)/expected_fiat_base_on_nominal_price
                    slipage = round(slipage, 6)

                    self.fiat_amount_recieved = fiat_bought
                    self.hash = tx_hash
                    self.uniswap_version = version
                    self.token_nominal_price = token_price
                    self.token_effective_price = self.fiat_amount_recieved / self.token_amount_spent
                    self.slipage = slipage
                    self.state = transaction_state_succesful
                    self.fee = round(tx_fee, 2)

                else:
                    self.state = transaction_state_failed
    
