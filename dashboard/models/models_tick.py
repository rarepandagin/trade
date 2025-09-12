from django.db import models
from dashboard.views_pages import toolkit as tk

class Tick(models.Model):
    id = models.BigAutoField(primary_key=True)

    epoch = models.BigIntegerField(default=0)

    data = models.JSONField(default=dict)



    def save(self, *args, **kwargs):

        self.epoch = tk.get_epoch_now()

        super(Tick, self).save(*args, **kwargs)
