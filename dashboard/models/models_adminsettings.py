from botocore import tokens
from django.db import models
from django.utils import choices
from ens.ens import default
from dashboard.models.coins import *


FastGasPrice = "FastGasPrice"
SafeGasPrice = "SafeGasPrice"
ProposeGasPrice = "ProposeGasPrice"

gas_speeds = {
    FastGasPrice : "FastGasPrice",
    ProposeGasPrice : "ProposeGasPrice",
    SafeGasPrice : "SafeGasPrice",
}


account_hedge = "account_hedge"
account_dex = "account_dex"
account_ajax = "account_ajax"
account_eagle = "account_eagle"
account_ranger = "account_ranger"
account_lion = "account_lion"
account_tiger = "account_tiger"

accounts = {
    
    account_hedge : "account_hedge",
    account_dex : "account_dex",
    account_ajax : "account_ajax",
    account_eagle : "account_eagle",
    account_ranger : "account_ranger",
    account_lion : "account_lion",
    account_tiger : "account_tiger",

}

vision_consensus_unsure = "vision_consensus_unsure"
vision_consensus_pro_long = "vision_consensus_pro_long"
vision_consensus_pro_short = "vision_consensus_pro_short"

vision_consensus_options = {
    vision_consensus_unsure: "vision_consensus_unsure",
    vision_consensus_pro_long: "vision_consensus_pro_long",
    vision_consensus_pro_short: "vision_consensus_pro_short",
}


allow_auto_purchase_none = "allow_auto_purchase_none"
allow_auto_purchase_safe = "allow_auto_purchase_safe"
allow_auto_purchase_pass = "allow_auto_purchase_pass"
allow_auto_purchase_all = "allow_auto_purchase_all"

allow_auto_purchase_options = {
    "allow_auto_purchase_none" : "allow_auto_purchase_none",
    "allow_auto_purchase_safe" : "allow_auto_purchase_safe",
    "allow_auto_purchase_pass" : "allow_auto_purchase_pass",
    "allow_auto_purchase_all" : "allow_auto_purchase_all"
}

class AdminSettings(models.Model):

    id = models.BigAutoField(primary_key=True)
    
    pulses_are_being_blocked = models.BooleanField(default=False)

    active_account = models.CharField(choices=accounts, default=account_hedge)

    # settings
    borrow_from_aave = models.BooleanField(default=False)
    
    alarms = models.BooleanField(default=True)

    interval = models.IntegerField(default=5, help_text="pulses interval in seconds")

    tx_tries = models.IntegerField(default=2, help_text="how many times a uniswap swap will repeat at max (in case of a failure)")

    secure_profit_ratio = models.FloatField(default=0.7, help_text="this is used to improve stop loss in case a profit take price is reached")

    max_sane_gas_price = models.FloatField(default=4.0, help_text="maximum gas price under which all tx are allowed to execute")

    gas_speed = models.CharField(choices=gas_speeds, default=FastGasPrice)

    fiat_coin = models.CharField(choices=fiat_coins, default=usdc)


    ## AAVE settings
    aave_borrow_to_collateral_added_safety_ratio = models.FloatField(default=0.9, help_text="a safety margin to make sure we won't borrow all of the borrow amount")
    aave_info_update_pulse_steps    = models.IntegerField(      default=10, help_text="this is how many pulses to skip until the next update of aave user account data")
    pulse_counter                   = models.BigIntegerField(   default=0, help_text="this is used to keep track of updating the aave user data")
    aave_user_account_data          = models.JSONField(         default=dict, blank=True, null=True, help_text="results from aave contract method for user data is stored here")



    # calculated on demand
    balances = models.JSONField(default=dict, blank=True, null=True)

    uniswap_asm_fiat_to_token = models.FloatField(default=3)
    uniswap_asm_token_to_fiat = models.FloatField(default=3)

    sushiswap_asm_fiat_to_token = models.FloatField(default=3)
    sushiswap_asm_token_to_fiat = models.FloatField(default=3)

    # auto fill remotely
    prices = models.JSONField(default=dict, blank=True, null=True)
    gas = models.JSONField(default=dict, blank=True, null=True)
    
    prices_update_epoch = models.BigIntegerField(default=0)
    gas_update_epoch = models.BigIntegerField(default=0)
    gas_update_epoch_max_allowed_delay_seconds = models.IntegerField(default=30)





    # DEPTH
    depth_filtering_active      = models.BooleanField(default=True)
    depth_show_cumulative       = models.BooleanField(default=False)
    depth_lowest_price          = models.FloatField(default=4200)
    depth_highest_price         = models.FloatField(default=4400)
    depth_cluster_width_usd     = models.FloatField(default=1)


    # COMMAND
    command_function    = models.TextField(default='', blank=True, null=True)
    command_arguments   = models.JSONField(default=dict, blank=True, null=True)

    # INDICATORS
    INDICATORS                      = models.JSONField(default=list, blank=True, null=True)
    MINUTES                         = models.JSONField(default=list, blank=True, null=True)
    live_indicators                 = models.JSONField(default=dict, blank=True, null=True)
    
    active_time_frame_minutes       = models.IntegerField(default=1)
    active_time_frame_length        = models.IntegerField(default=1440)

    vision                          = models.JSONField(default=dict, blank=True, null=True)


    vision_consensus                = models.CharField(choices=vision_consensus_options, default=vision_consensus_unsure)



    # DEX
    tokens                                      = models.JSONField(default=list, blank=True, null=True)
    allow_auto_purchase                         = models.CharField(choices=allow_auto_purchase_options, default=allow_auto_purchase_none)
    auto_purchase_safe_token_fiat_amount        = models.FloatField(default=1)
    auto_purchase_pass_token_fiat_amount        = models.FloatField(default=1)