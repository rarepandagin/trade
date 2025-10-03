from django.db import models




class Tick(models.Model):
    id = models.BigAutoField(primary_key=True)

    epoch = models.BigIntegerField(default=0, unique=True)

    price = models.FloatField(default=0)

    indicator_ema_minutely_20   = models.FloatField(default=0)
    indicator_ema_minutely_50   = models.FloatField(default=0)
    indicator_ema_minutely_200  = models.FloatField(default=0)

    indicator_ema_hourly_20     = models.FloatField(default=0)
    indicator_ema_hourly_50     = models.FloatField(default=0)
    indicator_ema_hourly_200    = models.FloatField(default=0)



