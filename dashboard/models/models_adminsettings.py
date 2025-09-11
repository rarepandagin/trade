from django.db import models
from dashboard.models.coins import *

class AdminSettings(models.Model):

    id = models.BigAutoField(primary_key=True)
    
    pulses_are_being_blocked = models.BooleanField(default=False)

    # settings
    alarms = models.BooleanField(default=True)
    interval = models.IntegerField(default=5)
    tx_tries = models.IntegerField(default=2)
    secure_profit_ratio = models.FloatField(default=0.7)
    max_sane_gas_price = models.FloatField(default=4.0)



    fiat_coin = models.CharField(choices=fiat_coins, default=usdc)

    added_slipage_multiplier_fiat_to_coin = models.FloatField(default=3)
    added_slipage_multiplier_coin_to_fiat = models.FloatField(default=3)


    # calculated on demand
    balances = models.JSONField(default=dict, blank=True, null=True)

    # auto fill remotely
    prices = models.JSONField(default=dict, blank=True, null=True)
    gas = models.JSONField(default=dict, blank=True, null=True)
    
    prices_update_epoch = models.BigIntegerField(default=0)
    gas_update_epoch = models.BigIntegerField(default=0)


    depth_filtering_active      = models.BooleanField(default=True)
    depth_show_cumulative       = models.BooleanField(default=False)
    depth_lowest_price          = models.FloatField(default=4200)
    depth_highest_price         = models.FloatField(default=4400)
    depth_cluster_width_usd     = models.FloatField(default=1)
