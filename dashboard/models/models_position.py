from django.db import models
from traceback import format_exc
from dashboard.views_pages import toolkit as tk
from dashboard.views_pages import transaction_dispatch
from dashboard.models import models_position
import copy

from dashboard.models.coins import *
from dashboard.models import models_order

in_loss = "in_loss"
reaching_profit_take_price = "reaching_profit_take_price"
post_profit_take_price = "post_profit_take_price"
exited_in_loss = "exited_in_loss"
exited_in_profit = "exited_in_profit"

position_states = {
    in_loss : "in_loss",
    reaching_profit_take_price : "reaching_profit_take_price",
    post_profit_take_price : "post_profit_take_price",
    exited_in_loss : "exited_in_loss",
    exited_in_profit : "exited_in_profit",
}



class Position(models.Model):

    id = models.BigAutoField(primary_key=True)

    # initial setup
    order = models.ForeignKey(models_order.Order, on_delete=models.SET_NULL, null=True)

    coin_amount = models.FloatField(default=0)

    entry_price = models.FloatField(default=0)

    profit_take_price = models.FloatField(default=0)

    stop_loss_price = models.FloatField(default=0)
    
    initial_stop_loss_price = models.FloatField(default=0)




    # auto
    uuid        = models.TextField(default="", null=True, blank=True)
    active      = models.BooleanField(default=True)
    state       = models.CharField(choices=position_states, default=reaching_profit_take_price)
    exit_price  = models.FloatField(default=0)
    stop_loss_price_improved = models.BooleanField(default=False)

    profit_amount_at_profit_take_price      = models.FloatField(default=0)
    loss_amount_at_stop_loss_price          = models.FloatField(default=0)
    ambition_ratio                          = models.FloatField(default=0)

    # collected and calculated
    price       = models.FloatField(default=0)
    value       = models.FloatField(default=0, null=True, blank=True)
    growth_usd  = models.FloatField(default=0, null=True, blank=True)
    final_profit_usd = models.FloatField(default=0)

    growth_percentage_from_entry_price              = models.FloatField(default=0, null=True, blank=True)




    # automatic

    epoch_created = models.BigIntegerField(default=0)
    epoch_updated = models.BigIntegerField(default=0)
    epoch_closed = models.BigIntegerField(default=0)


    # settings
    display_on_chart = models.BooleanField(default=False)
    # auto_exit = models.BooleanField(default=False)
    auto_exit_style     = models.CharField(choices=models_order.auto_exit_styles,   default=models_order.auto_exit_style_both_ways)

    archived = models.BooleanField(default=False)

    exited_gracefully = models.BooleanField(default=False)


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

        self.profit_take_price          = round(self.profit_take_price, 2)
        self.stop_loss_price            = round(self.stop_loss_price, 2)
        self.initial_stop_loss_price    = round(self.initial_stop_loss_price, 2)

        self.entry_price                = round(self.entry_price, 2)
        self.exit_price                 = round(self.exit_price, 2)

        self.profit_amount_at_profit_take_price             = round(self.profit_amount_at_profit_take_price, 2)
        self.loss_amount_at_stop_loss_price                 = round(self.loss_amount_at_stop_loss_price, 2)
        self.ambition_ratio                                 = round(self.ambition_ratio, 2)

        super(Position, self).save(*args, **kwargs)



    def exit_position(self):
        from dashboard.models import models_transaction

        self.auto_exit_style = models_order.auto_exit_style_never
        self.save()

        
        tk.send_message_to_frontend_dashboard(topic='display_toaster', payload={'message': f'exiting position {self.order.name}', 'color': 'green'})


        new_transaction = transaction_dispatch.create_and_actualize_uniswap_token_to_fiat_transaction(self.coin_amount, self.order.coin)



        if new_transaction.state == models_transaction.transaction_state_successful:


            self.exit_price = new_transaction.token_effective_price

            # identify all transactions that belong to this position and sum their gas fees
            total_gas_fees = sum([x.fee for x in models_transaction.Transaction.objects.filter(order=self.order)])

            self.final_profit_usd = new_transaction.fiat_amount_received - self.order.entry_capital - total_gas_fees

            self.active = False
            self.exited_gracefully = True
            self.save()


            # new_event = models_event.Event(
            #         position=self,
            #         description=f"exited\nprofit: {self.final_profit_usd}",
            #         event_type=models_event.exited,
            #         needs_notification=True,
            #     )
            # new_event.save()


        else:

            tk.create_new_notification(title="TX Failed while exiting position", message=f"tx for position {self.order.name} failed at execution")






    def description(self):
        return f"{self.order.name} ({self.state})"


    def reset(self):
        self.state = reaching_profit_take_price
        self.stop_loss_price_improved = False
        self.stop_loss_price = self.initial_stop_loss_price

    def evaluate_long(self):
        try:
            
            if self.profit_take_price < self.price:

                # increase the stop_loss_price
                # stop_loss_price. it never decreases; only increases

                previous_stop_loss = copy.deepcopy(self.stop_loss_price)

                admin_settings = tk.get_admin_settings()

                readjusted_stop_loss = self.entry_price + admin_settings.secure_profit_ratio * (self.price - self.entry_price)

                self.stop_loss_price = max(self.stop_loss_price, readjusted_stop_loss)

                if previous_stop_loss < self.stop_loss_price:

                    if not self.stop_loss_price_improved:
                        message_content = f"{self.order.name} reached profit take price"
                        tk.create_new_notification('Good news', message_content)
                        tk.send_message_to_frontend_dashboard(topic='display_toaster', payload={'message': message_content, 'color': 'green'})


                    self.stop_loss_price_improved = True

                    self.state = models_position.post_profit_take_price

                    tk.send_message_to_frontend_dashboard(topic='display_toaster', payload={'message': f'stop loss improved for position {self.order.name}', 'color': 'green'})



            if self.price < self.entry_price:
                self.state = models_position.in_loss

            else:
                if self.stop_loss_price_improved:

                    self.state = models_position.post_profit_take_price
                else:
                    self.state = models_position.reaching_profit_take_price



            self.profit_amount_at_profit_take_price = (self.profit_take_price - self.entry_price) * self.coin_amount
            self.loss_amount_at_stop_loss_price = (self.entry_price - self.stop_loss_price) * self.coin_amount
            self.ambition_ratio = abs(self.profit_amount_at_profit_take_price / self.loss_amount_at_stop_loss_price)


            # EXIT
            if self.price < self.stop_loss_price:
                if self.auto_exit_style in [models_order.auto_exit_style_both_ways, models_order.auto_exit_style_only_after_stop_loss_price_reached]:

                    self.exit_position()

                elif self.auto_exit_style == models_order.auto_exit_style_only_after_profit_take_price_reached:
                    if self.stop_loss_price_improved:
                        self.exit_position()



            delta_price = self.price - self.entry_price
            self.value                              = self.price * self.coin_amount
            self.growth_usd                         = delta_price * self.coin_amount
            self.growth_percentage_from_entry_price = 100 * delta_price / self.entry_price
            
        
        except:
            tk.create_new_notification("runtime error", format_exc())



    def evaluate_short(self):
        try:
            
            #
            # if self.profit_take_price < self.price:

            if self.price < self.profit_take_price:

                # decrease the stop_loss_price
                # stop_loss_price. it never increases; only decreases

                previous_stop_loss = copy.deepcopy(self.stop_loss_price)

                admin_settings = tk.get_admin_settings()

                # readjusted_stop_loss = self.entry_price + admin_settings.secure_profit_ratio * (self.price - self.entry_price)
                readjusted_stop_loss = self.price + (1.0 - admin_settings.secure_profit_ratio) * (self.entry_price - self.price)

                # self.stop_loss_price = max(self.stop_loss_price, readjusted_stop_loss)
                self.stop_loss_price = min(self.stop_loss_price, readjusted_stop_loss)

                # if previous_stop_loss < self.stop_loss_price:
                if self.stop_loss_price < previous_stop_loss:

                    if not self.stop_loss_price_improved:
                        message_content = f"{self.order.name} reached profit take price"
                        tk.create_new_notification('Good news', message_content)
                        tk.send_message_to_frontend_dashboard(topic='display_toaster', payload={'message': message_content, 'color': 'green'})


                    self.stop_loss_price_improved = True

                    self.state = models_position.post_profit_take_price

                    tk.send_message_to_frontend_dashboard(topic='display_toaster', payload={'message': f'stop loss improved for position {self.order.name}', 'color': 'green'})



            # if self.price < self.entry_price:
            if self.price > self.entry_price:
                self.state = models_position.in_loss

            else:
                if self.stop_loss_price_improved:

                    self.state = models_position.post_profit_take_price
                else:
                    self.state = models_position.reaching_profit_take_price



            # self.profit_amount_at_profit_take_price = (self.profit_take_price - self.entry_price) * self.coin_amount
            # self.loss_amount_at_stop_loss_price = (self.entry_price - self.stop_loss_price) * self.coin_amount
            self.profit_amount_at_profit_take_price = (self.entry_price - self.profit_take_price) * self.coin_amount
            self.loss_amount_at_stop_loss_price = (self.stop_loss_price - self.entry_price) * self.coin_amount


            self.ambition_ratio = abs(self.profit_amount_at_profit_take_price / self.loss_amount_at_stop_loss_price)


            # EXIT
            # if self.price < self.stop_loss_price:
            if self.price > self.stop_loss_price:
                if self.auto_exit_style in [models_order.auto_exit_style_both_ways, models_order.auto_exit_style_only_after_stop_loss_price_reached]:

                    self.exit_position()

                elif self.auto_exit_style == models_order.auto_exit_style_only_after_profit_take_price_reached:
                    if self.stop_loss_price_improved:
                        self.exit_position()




            # delta_price = self.price - self.entry_price
            delta_price = self.entry_price - self.price
            self.value                              = self.price * self.coin_amount
            self.growth_usd                         = delta_price * self.coin_amount
            self.growth_percentage_from_entry_price = 100 * delta_price / self.entry_price
            

        except:
            tk.create_new_notification("runtime error", format_exc())



