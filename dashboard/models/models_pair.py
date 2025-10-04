from django.db import models

from dashboard.views_pages import toolkit as tk
from dashboard.models import models_position


class Pair(models.Model):
    id = models.BigAutoField(primary_key=True)

    uuid = models.TextField(default="", null=True, blank=True)
    
    long_position   = models.ForeignKey(models_position.Position,   on_delete=models.SET_NULL, null=True, related_name='long_position')
    short_position  = models.ForeignKey(models_position.Position,   on_delete=models.SET_NULL, null=True, related_name='short_position')


    epoch_created = models.BigIntegerField(default=0)


    def save(self, *args, **kwargs):
        if self.uuid == '':
            self.uuid = tk.get_new_uuid()
            self.epoch_created = tk.get_epoch_now()


        super(Pair, self).save(*args, **kwargs)

