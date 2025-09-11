from django.db import models
from traceback import format_exc
from dashboard.views_pages import toolkit as tk

from dashboard.models.coins import *


auto_exit_style_both_ways = "auto_exit_style_both_ways"
auto_exit_style_only_after_min_profit = "auto_exit_style_only_after_min_profit"
auto_exit_style_only_below_stop_loss = "auto_exit_style_only_below_stop_loss"
auto_exit_style_never = "auto_exit_style_never"


auto_exit_styles = {
    auto_exit_style_both_ways : "auto_exit_style_both_ways",
    auto_exit_style_only_after_min_profit : "auto_exit_style_only_after_min_profit",
    auto_exit_style_only_below_stop_loss : "auto_exit_style_only_below_stop_loss",
    auto_exit_style_never: "auto_exit_style_never",
}

buy_if_price_is_above = "buy_if_price_is_above"
buy_if_price_is_below = "buy_if_price_is_below"

order_modes = {
    buy_if_price_is_above : "buy_if_price_is_above",
    buy_if_price_is_below : "buy_if_price_is_below",
}

class Order(models.Model):

    id = models.BigAutoField(primary_key=True)

    # initial setup

    name = models.TextField(default="", null=True, blank=True)

    coin = models.CharField(choices=coins, default=weth)

    mode = models.CharField(choices=order_modes, default=buy_if_price_is_below)

    entry_capital = models.FloatField(default=0)

    order_price = models.FloatField(default=0)

    min_profit_exit_price = models.FloatField(default=0)

    stop_loss_price = models.FloatField(default=0)
    




    # auto
    uuid = models.TextField(default="", null=True, blank=True)
    active = models.BooleanField(default=True)
    executed = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)
    fullfiled = models.BooleanField(default=False)


    # automatic
    epoch_created = models.BigIntegerField(default=0)
    epoch_updated = models.BigIntegerField(default=0)
    epoch_executed = models.BigIntegerField(default=0)


    # settings
    # auto_exit = models.BooleanField(default=False)
    auto_exit_style     = models.CharField(choices=auto_exit_styles,   default=auto_exit_style_only_after_min_profit)



    def __str__(self):
        return self.name


    def save(self, *args, **kwargs):
        if self.uuid == '':
            self.uuid = tk.get_new_uuid()
            self.epoch_created = tk.get_epoch_now()

        else:
            self.epoch_updated = tk.get_epoch_now()

        self.order_price                = round(self.order_price, 2)
        self.stop_loss_price            = round(self.stop_loss_price, 2)
        self.min_profit_exit_price      = round(self.min_profit_exit_price, 2)
        

        super(Order, self).save(*args, **kwargs)



    def execute(self):
        from dashboard.models import models_position
        from dashboard.models import models_transaction

        if self.active and (not self.fullfiled):

            new_transaction = tk.create_fiat_to_token_transaction(self.entry_capital, self.coin)


            if new_transaction.state == models_transaction.transaction_state_succesful:

                new_position = models_position.Position(
                    order=self,

                    coin_amount = new_transaction.token_amount_recieved,

                    entry_price=new_transaction.token_effective_price,

                    min_profit_exit_price = self.min_profit_exit_price,
                    stop_loss_price = self.stop_loss_price,
                    initial_stop_loss_price = self.stop_loss_price,
                )

                new_position.save()

                new_transaction.position = new_position
                new_transaction.save()

                self.fullfiled = True
                tk.create_new_notification(title="Buy order fulfilled", message=f"order {self.name} fulfilled")

            else:
                self.fullfiled = False
                tk.create_new_notification(title="Buy order did not get fulfilled due to tx failure", message=f"tx for order {self.name} failed at execution")


            self.active = False
            self.executed = True


    def evaluate(self):
        try:
            if self.active and (not self.executed):
    
                admin_settings = tk.get_admin_settings()

                if self.mode == buy_if_price_is_below:
                    if admin_settings.prices[self.coin.lower()] < self.order_price :
                        self.execute()

                elif self.mode == buy_if_price_is_above:
                    if self.order_price < admin_settings.prices[self.coin.lower()] :
                        self.execute()  

        except:
            tk.create_new_notification("runtime error", format_exc())

        

