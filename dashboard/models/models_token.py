from django.db import models
from ens.ens import default
from dashboard.views_pages import toolkit as tk

from dashboard.modules.dapps.uniswap.uniswap_class import Uniswap
from dashboard.modules.dapps.sushiswap.sushiswap_class import Sushiswap
from dashboard.modules.dapps.aave.aave_class import Aave
from dashboard.modules.dapps.arbi.arbi_class import Arbi

from dashboard.models.coins import *



class Token(models.Model):

    id = models.BigAutoField(primary_key=True)
    
    
    # DISCOVERY / INTRINSIC
    contract                = models.TextField(null=True, blank=True ,           unique=True)
    event_block_number      = models.BigIntegerField(null=True, blank=True)
    pair_creation_epoch     = models.BigIntegerField(null=True, blank=True)

    pair_address            = models.TextField(null=True, blank=True)

    name                    = models.TextField(null=True, blank=True)
    decimals                = models.IntegerField(null=True, blank=True)
    symbol                  = models.TextField(null=True, blank=True)
    total_supply            = models.FloatField(null=True, blank=True)
    weth_idx_in_pair        = models.IntegerField(null=True, blank=True)
    epoch_created           = models.BigIntegerField(null=True, blank=True)


    # PAIR DYNAMICS

    weth_pair_reserves      = models.FloatField(null=True, blank=True)
    price_per_weth          = models.FloatField(null=True, blank=True)
    volume                  = models.FloatField(default=0, null=True, blank=True)



    # INVESTIGATING / DYNAMIC
    # every token in investigated consistently unless keep_investigating is set to false
    # keep_investigating is set to false where there is enough reason for dismissing the token
    # we do not delete the token record so that its contract address is maintained
    # we also stop investigating when investigation_pass is set to True


    uncx_user               = models.TextField(null=True, blank=True)
    uncx_token_amount       = models.FloatField(default=0, null=True, blank=True)
    uncx_pool_lock_ratio    = models.FloatField(default=0, null=True, blank=True)
    uncx_epoch_start_lock   = models.BigIntegerField(default=0, null=True, blank=True)
    uncx_epoch_end_lock     = models.BigIntegerField(default=0, null=True, blank=True)


    go_plus_lp_total_supply = models.FloatField(default=0, null=True, blank=True)
    go_plus_locked_lp_ratio = models.FloatField(default=0, null=True, blank=True)
    go_plus_dex_liquidity   = models.FloatField(default=0, null=True, blank=True)
    go_plus_security_issues = models.JSONField(default=list, null=True, blank=True)

    keep_investigating      = models.BooleanField(default=True, null=True, blank=True)
    epoch_investigated      = models.BigIntegerField( default=0, null=True, blank=True)
    investigation_pass      = models.BooleanField(default= False, null=True, blank=True)
    investigation_safe      = models.BooleanField(default= False, null=True, blank=True)
    investigation_red_flag  = models.BooleanField(default=False)
    investigated            = models.BooleanField(default=False)



    # admin actions
    # these are field used in manual operations 
    price                = models.FloatField(default=0, null=True, blank=True)

    show        = models.BooleanField(default=True, null=True, blank=True)
    show_on_chart = models.BooleanField(default=True, null=True, blank=True)
    imported    = models.BooleanField(default=False, null=True, blank=True)
    
    balance                 = models.FloatField(default=0, blank=True, null=True)
    approved                = models.BooleanField(default=False, null=True, blank=True)

    auto_purchased          = models.BooleanField(default=False, null=True, blank=True)
    already_alerted          = models.BooleanField(default=False, null=True, blank=True)