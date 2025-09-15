from django.contrib import admin
from django.contrib.auth.models import User

# Register your models here.
from dashboard.models import *


admin.site.register(Event)
admin.site.register(AdminSettings)
admin.site.register(Tick)





class adminViewTransaction(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'state',
        'transaction_type',
        'uniswap_version',
        'position',
        'fiat_amount_spent',
        'token_amount_recieved',
        'token_amount_spent',
        'fiat_amount_recieved',
        'token_nominal_price',
        'token_effective_price',
        'slipage',
        'fee',
        )
admin.site.register(Transaction, adminViewTransaction)



class adminViewOrder(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'epoch_created',
        'mode',
        'entry_capital',
        'order_price',
        'min_profit_exit_price',
        'stop_loss_price',
        'active',
        'executed',
        'fullfiled',
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




class adminViewAlert(admin.ModelAdmin):
    list_display = (
        'id',
        'epoch_created',
        'alert_type',
        'alert_price',
        'executed',
        )
admin.site.register(Alert, adminViewAlert)


