from django.db import models
from traceback import format_exc
from dashboard.views_pages import toolkit as tk
from dashboard.models import models_position
import copy

from dashboard.models.coins import *
from dashboard.models import models_order

in_loss = "in_loss"
reaching_min_profit_exit_price = "reaching_min_profit_exit_price"
post_min_profit_exit_price = "post_min_profit_exit_price"
exited_in_loss = "exited_in_loss"
exited_in_profit = "exited_in_profit"

position_states = {
    in_loss : "in_loss",
    reaching_min_profit_exit_price : "reaching_min_profit_exit_price",
    post_min_profit_exit_price : "post_min_profit_exit_price",
    exited_in_loss : "exited_in_loss",
    exited_in_profit : "exited_in_profit",
}



class Position(models.Model):

    id = models.BigAutoField(primary_key=True)

    # initial setup
    order = models.ForeignKey(models_order.Order, on_delete=models.SET_NULL, null=True)

    coin_amount = models.FloatField(default=0)

    entry_price = models.FloatField(default=0)

    min_profit_exit_price = models.FloatField(default=0)

    stop_loss_price = models.FloatField(default=0)
    
    initial_stop_loss_price = models.FloatField(default=0)




    # auto
    uuid = models.TextField(default="", null=True, blank=True)
    active = models.BooleanField(default=True)
    state = models.CharField(choices=position_states, default=reaching_min_profit_exit_price)
    exit_price = models.FloatField(default=0)
    stop_loss_price_increased = models.BooleanField(default=False)

    profit_amount_at_min_profit_exit_price  = models.FloatField(default=0)
    loss_amount_at_stop_loss_price          = models.FloatField(default=0)
    ambition_ratio                             = models.FloatField(default=0)

    # calculated
    price = models.FloatField(default=0)
    value = models.FloatField(default=0, null=True, blank=True)
    growth_usd = models.FloatField(default=0, null=True, blank=True)
    
    growth_percentage_from_entry_price              = models.FloatField(default=0, null=True, blank=True)
    growth_percentage_from_stop_loss_price          = models.FloatField(default=0, null=True, blank=True)
    growth_percentage_from_min_profit_exit_price    = models.FloatField(default=0, null=True, blank=True)




    # automatic
    final_profit_usd = models.FloatField(default=0)

    epoch_created = models.BigIntegerField(default=0)
    epoch_updated = models.BigIntegerField(default=0)
    epoch_closed = models.BigIntegerField(default=0)


    # settings
    display_on_chart = models.BooleanField(default=True)
    # auto_exit = models.BooleanField(default=False)
    auto_exit_style     = models.CharField(choices=models_order.auto_exit_styles,   default=models_order.auto_exit_style_only_after_min_profit)



    def __str__(self):
        return self.description()


    def save(self, *args, **kwargs):
        if self.uuid == '':
            self.uuid = tk.get_new_uuid()
            self.epoch_created = tk.get_epoch_now()

        else:
            self.epoch_updated = tk.get_epoch_now()

        self.value                  = round(self.value, 2)
        self.growth_usd             = round(self.growth_usd, 2)
        self.final_profit_usd       = round(self.final_profit_usd, 2)

        self.growth_percentage_from_entry_price             = round(self.growth_percentage_from_entry_price, 2)
        self.growth_percentage_from_stop_loss_price         = round(self.growth_percentage_from_stop_loss_price, 2)
        self.growth_percentage_from_min_profit_exit_price   = round(self.growth_percentage_from_min_profit_exit_price, 2)
        
        self.entry_price                = round(self.entry_price, 2)
        self.stop_loss_price            = round(self.stop_loss_price, 2)
        self.initial_stop_loss_price    = round(self.initial_stop_loss_price, 2)
        self.min_profit_exit_price    = round(self.min_profit_exit_price, 2)
        self.exit_price                 = round(self.exit_price, 2)
        
        self.profit_amount_at_min_profit_exit_price         = round(self.profit_amount_at_min_profit_exit_price, 2)
        self.loss_amount_at_stop_loss_price                 = round(self.loss_amount_at_stop_loss_price, 2)
        self.ambition_ratio                                    = round(self.ambition_ratio, 2)

        super(Position, self).save(*args, **kwargs)



    def exit_position(self):
        from dashboard.models import models_event
        from dashboard.models import models_transaction


        new_transaction = tk.create_token_to_fiat_transaction(self.coin_amount, self.order.coin)

        new_transaction.position = self
        new_transaction.save()

        if new_transaction.state == models_transaction.transaction_state_succesful:


            self.exit_price = new_transaction.token_effective_price

            # identify all transactions that belong to this position and sum their gas fees
            total_gas_fees = sum([x.fee for x in models_transaction.Transaction.objects.filter(position=self)])

            self.final_profit_usd = new_transaction.fiat_amount_recieved - self.order.entry_capital - total_gas_fees

            self.active = False
            self.save()


            new_event = models_event.Event(
                    position=self,
                    description=f"exited\nprofit: {self.final_profit_usd}",
                    event_type=models_event.exited,
                    needs_notification=True,
                )
            new_event.save()


        else:
            self.active = False
            self.save()

            tk.create_new_notification(title="TX Failed whilte exiting position", message=f"tx for position {self.order.name} failed at execution")






    def description(self):
        return f"{self.order.name} ({self.state})"


    def reset(self):
        self.state = reaching_min_profit_exit_price
        self.stop_loss_price_increased = False
        self.stop_loss_price = self.initial_stop_loss_price

    def evaluate(self):
        try:
            from dashboard.models import models_event
            
            if self.min_profit_exit_price < self.price:

                # increase the stop_loss_price
                # stop_loss_price never decreses; only increases

                previous_stop_loss = copy.deepcopy(self.stop_loss_price)

                admin_settings = tk.get_admin_settings()

                # readjusted_stop_loss = self.price - 15
                # readjusted_stop_loss = 0.7 * (self.price - self.entry_price)
                readjusted_stop_loss = self.entry_price + admin_settings.secure_profit_ratio * (self.price - self.entry_price)

                self.stop_loss_price = max(self.stop_loss_price, readjusted_stop_loss)

                if previous_stop_loss < self.stop_loss_price:

                    if not self.stop_loss_price_increased:
                        tk.create_new_notification('Good news', f"{self.name} reached min profit price")


                    self.stop_loss_price_increased = True

                    self.state = models_position.post_min_profit_exit_price

                    new_event = models_event.Event(
                            position=self,
                            description=f"stop loss increased from {round(previous_stop_loss, 2)} to {round(self.stop_loss_price, 2)}",
                            event_type=models_event.stop_loss_price_increased,
                        )
                    new_event.save()



            if self.price < self.entry_price:
                self.state = models_position.in_loss
            else:
                if self.stop_loss_price_increased:

                    self.state = models_position.post_min_profit_exit_price
                else:
                    self.state = models_position.reaching_min_profit_exit_price



            self.profit_amount_at_min_profit_exit_price = (self.min_profit_exit_price - self.entry_price) * self.coin_amount
            self.loss_amount_at_stop_loss_price = (self.entry_price - self.stop_loss_price) * self.coin_amount
            self.ambition_ratio = abs(self.profit_amount_at_min_profit_exit_price / self.loss_amount_at_stop_loss_price)


            # EXIT
            if self.price < self.stop_loss_price:
                # exiting:
                if self.auto_exit_style in [models_order.auto_exit_style_both_ways, models_order.auto_exit_style_only_below_stop_loss]:

                    self.exit_position()

                elif self.auto_exit_style == models_order.auto_exit_style_only_after_min_profit:
                    if self.stop_loss_price_increased:
                        self.exit_position()




            self.value                              = self.price * self.coin_amount
            self.growth_usd                         = (self.price - self.entry_price) * self.coin_amount
            self.growth_percentage_from_entry_price = 100 * (self.price - self.entry_price) / self.entry_price
            
            self.growth_percentage_from_stop_loss_price         = 100 * (self.price - self.stop_loss_price) / (self.min_profit_exit_price - self.stop_loss_price)
            self.growth_percentage_from_min_profit_exit_price   = 100 * (self.price - self.entry_price)     / (self.min_profit_exit_price - self.entry_price)
        
        except:
            tk.create_new_notification("runtime error", format_exc())



