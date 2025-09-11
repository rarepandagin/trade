from django.db import models

from dashboard.views_pages import toolkit as tk


from dashboard.models import models_position


KLINE_INTERVAL_1MINUTE  = '1m'
KLINE_INTERVAL_3MINUTE  = '3m'
KLINE_INTERVAL_5MINUTE  = '5m'
KLINE_INTERVAL_15MINUTE = '15m'
KLINE_INTERVAL_30MINUTE = '30m'
KLINE_INTERVAL_1HOUR    = '1h'

intervals = {
    KLINE_INTERVAL_1MINUTE  : '1m',
    KLINE_INTERVAL_3MINUTE  : '3m',
    KLINE_INTERVAL_5MINUTE  : '5m',
    KLINE_INTERVAL_15MINUTE : '15m',
    KLINE_INTERVAL_30MINUTE : '30m',
    KLINE_INTERVAL_1HOUR    : '1h'
}



class Candle(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.TextField(default="", null=True, blank=True)
    coin = models.CharField(choices=models_position.coins, default=models_position.weth)
    interval = models.CharField(choices=intervals, default=KLINE_INTERVAL_1MINUTE)

    open_time = models.BigIntegerField(default=0)

    open = models.FloatField(default=0)
    high = models.FloatField(default=0)
    low = models.FloatField(default=0)
    close = models.FloatField(default=0)
    volume = models.FloatField(default=0)

    close_time = models.BigIntegerField(default=0)


    def save(self, *args, **kwargs):
        if self.uuid == '':
            self.uuid = tk.get_new_uuid()

        super(Candle, self).save(*args, **kwargs)


