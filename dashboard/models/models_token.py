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

    # intrinsic properties
    # these fields are collected only once when the token is collected from DEXScreener
    chain_id      = models.TextField(default='', blank=True, null=True)
    address       = models.TextField(default='', blank=True, null=True)
    contract      = models.TextField(default='', blank=True, null=True, unique=True)
    url           = models.TextField(default='', blank=True, null=True)
    image_url     = models.TextField(default='', blank=True, null=True)

    name          = models.TextField(default='', blank=True, null=True)
    pair          = models.TextField(default='', blank=True, null=True)
    version       = models.TextField(default='', blank=True, null=True)
    epoch_created = models.BigIntegerField(default=0, blank=True, null=True)


    # ongoing evaluation
    # there fields are continuously monitored

    price                   = models.FloatField(default=0, blank=True, null=True)
    volume                  = models.FloatField(default=0, blank=True, null=True)
    makers                  = models.BigIntegerField(default=0, blank=True, null=True)
    liquidity               = models.FloatField(default=0, blank=True, null=True)
    cap                     = models.FloatField(default=0, blank=True, null=True)
    locked_liquidity        = models.BooleanField(default=False)
    has_website             = models.BooleanField(default=False)
    has_twitter             = models.BooleanField(default=False)
    has_telegram            = models.BooleanField(default=False)
    go_security             = models.BooleanField(default=False)
    quick_intel             = models.BooleanField(default=False)
    token_sniffer           = models.BooleanField(default=False)
    honeypot_is             = models.BooleanField(default=False)



    # admin actions
    # these are field used in manual operations 
    show        = models.BooleanField(default=True)
    show_on_chart = models.BooleanField(default=True)
    imported    = models.BooleanField(default=False)
    
    balance                 = models.FloatField(default=0, blank=True, null=True)
    approved                = models.BooleanField(default=False)

    auto_purchased          = models.BooleanField(default=False)
    already_alerted          = models.BooleanField(default=False)