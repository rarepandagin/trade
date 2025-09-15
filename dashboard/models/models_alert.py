from django.db import models

from dashboard.views_pages import toolkit as tk

from dashboard.models import models_position

price_goes_above = "price_goes_above"
price_goes_below = "price_goes_below"

alert_types = {
    price_goes_above : "price_goes_above",
    price_goes_below : "price_goes_below",
}


class Alert(models.Model):
    id = models.BigAutoField(primary_key=True)

    uuid = models.TextField(default="", null=True, blank=True)
    
    alert_type = models.CharField(choices=alert_types, default=price_goes_above)
    
    alert_price = models.FloatField(default=0)

    epoch_created = models.BigIntegerField(default=0)

    executed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.uuid == '':
            self.uuid = tk.get_new_uuid()
            self.epoch_created = tk.get_epoch_now()


        super(Alert, self).save(*args, **kwargs)

    
    def brief(self):
        return f"{self.alert_type} {self.alert_price}"


    def execute(self):
        if not self.executed:
            self.executed = True
            tk.create_new_notification(title="Alert", message=self.brief())



    def evaluate(self):

        if not self.executed:

            need_to_execute = False

            admin_settings = tk.get_admin_settings()

            if admin_settings.alarms:
                if self.alert_type == price_goes_above:
                    if admin_settings.prices['weth'] >= self.alert_price:
                        need_to_execute = True
                elif self.alert_type == price_goes_below:
                    if admin_settings.prices['weth'] <= self.alert_price:
                        need_to_execute = True

            if need_to_execute:
                self.execute()
                