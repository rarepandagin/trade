from django.contrib import admin
from django.contrib.auth.models import User

# Register your models here.
from dashboard.models import *


admin.site.register(Event)
admin.site.register(AdminSettings)



class adminViewCandle(admin.ModelAdmin):
    list_display = ('id', 'coin', 'interval', 'open_time', 'close_time')
admin.site.register(Candle, adminViewCandle)

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

class adminViewPosition(admin.ModelAdmin):
    list_display = ('id', 'name', 'coin', 'coin_amount')
admin.site.register(Position, adminViewPosition)


