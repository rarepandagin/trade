from django.contrib import admin
from django.contrib.auth.models import User

# Register your models here.
from dashboard.models import *


# admin.site.register(Event)
admin.site.register(AdminSettings)
# admin.site.register(Tick)
admin.site.register(Pair)
admin.site.register(Alert)
# admin.site.register(Price)





class adminViewTransaction(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'state',
        'transaction_type',
        'uniswap_version',
        'order',
        'fiat_amount_spent',
        'token_amount_received',
        'token_amount_spent',
        'fiat_amount_received',
        'token_nominal_price',
        'token_effective_price',
        'slippage',
        'fee',
        )
admin.site.register(Transaction, adminViewTransaction)



class adminViewOrder(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'epoch_created',
        'entry_condition',
        'entry_capital',
        'order_entry_price',
        'profit_take_price',
        'stop_loss_price',
        'active',
        'executed',
        'fulfilled',
        )
admin.site.register(Order, adminViewOrder)




class adminViewPosition(admin.ModelAdmin):
    list_display = (
        'id',
        'epoch_created',
        'state',
        'active',
        'archived',
        'final_profit_usd',
        )
admin.site.register(Position, adminViewPosition)





