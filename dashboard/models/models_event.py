from django.db import models

from dashboard.views_pages import toolkit as tk

from dashboard.models import models_position

stop_loss_price_improved = "stop_loss_price_improved"
exited = "exited"
stop_loss_price_occured_but_auto_exit_is_off = "stop_loss_price_occured_but_auto_exit_is_off"
transaction_failed = "transaction_failed"

event_types = {
    stop_loss_price_improved : "stop_loss_price_improved",
    stop_loss_price_occured_but_auto_exit_is_off : "stop_loss_price_occured_but_auto_exit_is_off",
    exited : "exited",
    transaction_failed : "transaction_failed",
}


class Event(models.Model):
    id = models.BigAutoField(primary_key=True)

    uuid = models.TextField(default="", null=True, blank=True)
    
    position = models.ForeignKey(models_position.Position, on_delete=models.SET_NULL, null=True)

    event_type = models.CharField(choices=event_types, default=stop_loss_price_improved)

    needs_notification = models.BooleanField(default=False)

    description = models.TextField(default="")

    epoch_created = models.BigIntegerField(default=0)


    def breif(self):
        return f"{self.position.description()}:\n{self.event_type}\n{self.description}"

    def save(self, *args, **kwargs):
        if self.uuid == '':
            self.uuid = tk.get_new_uuid()
            self.epoch_created = tk.get_epoch_now()

        if self.needs_notification:
            admin_settings = tk.get_admin_settings()

            if admin_settings.alarms:
                tk.create_new_notification(self.event_type, self.breif())
                


        super(Event, self).save(*args, **kwargs)
