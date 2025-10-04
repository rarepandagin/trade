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


    
    # long
    coin_amount_long = models.FloatField(default=0)
    
    #short
    coin_amount_borrowed_to_enter_short             = models.FloatField(default=0)
    fiat_amount_received_to_sell_and_enter_short    = models.FloatField(default=0)
    fiat_amount_spent_to_buy_and_exit_short         = models.FloatField(default=0)


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
    is_long     = models.BooleanField(default=False)

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



        tk.send_message_to_frontend_dashboard(topic='display_toaster', payload={'message': f'starting to exit position {self.order.name}', 'color': 'green'})

        if self.is_long:

            sell_transaction = transaction_dispatch.create_and_actualize_uniswap_token_to_fiat_transaction(token_to_fiat_amount=self.coin_amount_long, coin= self.order.coin)
            sell_transaction.order = self.order
            sell_transaction.save()
            
            if sell_transaction.state == models_transaction.transaction_state_successful:

                self.exit_price = sell_transaction.token_effective_price

                total_gas_fees = sum([x.fee for x in models_transaction.Transaction.objects.filter(order=self.order)])

                self.final_profit_usd = sell_transaction.fiat_amount_received - self.order.entry_capital - total_gas_fees

                self.active = False
                self.exited_gracefully = True
                self.save()


            else:
                tk.create_new_notification(title="Long position exit failed", message=f"sell tx for position {self.order.name} failed at execution")

        else:

            admin_settings = tk.get_admin_settings()
            live_price = admin_settings.prices[self.order.coin]

            self.fiat_amount_spent_to_buy_and_exit_short = self.coin_amount_borrowed_to_enter_short * live_price
            self.save()
            

            buy_transaction = transaction_dispatch.create_and_actualize_uniswap_fiat_to_token_transaction(
                    fiat_to_token_amount=self.fiat_amount_spent_to_buy_and_exit_short,
                    coin= self.order.coin
                )
            buy_transaction.order = self.order
            buy_transaction.save()

            if buy_transaction.state == models_transaction.transaction_state_successful:
                # now we need to repay the borrow

                repay_transaction = transaction_dispatch.create_and_actualize_aave_repay_transaction(
                    repay_amount=buy_transaction.token_amount_received
                )
                repay_transaction.order = self.order
                repay_transaction.save()

                if repay_transaction.state == models_transaction.transaction_state_successful:
                    
                    self.exit_price = buy_transaction.token_effective_price

                    total_gas_fees = sum([x.fee for x in models_transaction.Transaction.objects.filter(order=self.order)])

                    self.final_profit_usd = self.fiat_amount_received_to_sell_and_enter_short - self.fiat_amount_spent_to_buy_and_exit_short - total_gas_fees

                    self.active = False
                    self.exited_gracefully = True
                    self.save()

                else:
                    tk.create_new_notification(title="Short position exit failed", message=f"the token was purchased successfully but the repay tx for position {self.order.name} failed at execution")


            else:
                tk.create_new_notification(title="Short position exit failed", message=f"buy tx for position {self.order.name} failed at execution")





    def description(self):
        return f"{self.order.name} ({self.state})"


    def reset(self):
        self.state = reaching_profit_take_price
        self.stop_loss_price_improved = False
        self.stop_loss_price = self.initial_stop_loss_price

    def evaluate(self):
        try:

            profit_take_price_condition = False
            if self.is_long:
                profit_take_price_condition = self.profit_take_price < self.price
            else:
                profit_take_price_condition = self.price < self.profit_take_price

            
            if profit_take_price_condition:


                """
                for a long position:
                    increase the stop_loss_price
                    stop_loss_price. it never decreases; only increases
                
                for a short position:
                    decrease the stop_loss_price
                    stop_loss_price. it never increases; only decreases
                """

                previous_stop_loss = copy.deepcopy(self.stop_loss_price)

                admin_settings = tk.get_admin_settings()

                if self.is_long:
                    readjusted_stop_loss = self.entry_price + admin_settings.secure_profit_ratio * (self.price - self.entry_price)
                    self.stop_loss_price = max(self.stop_loss_price, readjusted_stop_loss)

                else:
                    readjusted_stop_loss = self.price + (1.0 - admin_settings.secure_profit_ratio) * (self.entry_price - self.price)
                    self.stop_loss_price = min(self.stop_loss_price, readjusted_stop_loss)


                stop_loss_price_update_condition = False
                if self.is_long:
                    stop_loss_price_update_condition = previous_stop_loss < self.stop_loss_price
                else:
                    stop_loss_price_update_condition = self.stop_loss_price < previous_stop_loss


                if stop_loss_price_update_condition:

                    if not self.stop_loss_price_improved:
                        message_content = f"{self.order.name} reached profit take price"
                        tk.create_new_notification('Good news', message_content)
                        tk.send_message_to_frontend_dashboard(topic='display_toaster', payload={'message': message_content, 'color': 'green'})


                    self.stop_loss_price_improved = True

                    self.state = models_position.post_profit_take_price

                    tk.send_message_to_frontend_dashboard(topic='display_toaster', payload={'message': f'stop loss improved for position {self.order.name}', 'color': 'green'})




            stop_loss_condition = False
            if self.is_long:
                stop_loss_condition = self.price < self.entry_price
            else:
                stop_loss_condition = self.price > self.entry_price


            if stop_loss_condition:
                self.state = models_position.in_loss

            else:
                if self.stop_loss_price_improved:

                    self.state = models_position.post_profit_take_price
                else:
                    self.state = models_position.reaching_profit_take_price


            if self.is_long:
                self.profit_amount_at_profit_take_price = (self.profit_take_price - self.entry_price) * self.coin_amount_long
                self.loss_amount_at_stop_loss_price = (self.entry_price - self.stop_loss_price) * self.coin_amount_long
            else:
                self.profit_amount_at_profit_take_price = (self.entry_price - self.profit_take_price) * self.coin_amount_borrowed_to_enter_short
                self.loss_amount_at_stop_loss_price = (self.stop_loss_price - self.entry_price) * self.coin_amount_borrowed_to_enter_short

            
            self.ambition_ratio = abs(self.profit_amount_at_profit_take_price / self.loss_amount_at_stop_loss_price)


            # EXIT
            
            exit_condition = False
            if self.is_long:
                exit_condition = self.price < self.stop_loss_price
            else:
                exit_condition = self.price > self.stop_loss_price



            if exit_condition:
                if self.auto_exit_style in [models_order.auto_exit_style_both_ways, models_order.auto_exit_style_only_after_stop_loss_price_reached]:

                    self.exit_position()

                elif self.auto_exit_style == models_order.auto_exit_style_only_after_profit_take_price_reached:
                    if self.stop_loss_price_improved:
                        self.exit_position()


            if self.is_long:
                delta_price = self.price - self.entry_price
                self.value                              = self.price * self.coin_amount_long
                self.growth_usd                         = delta_price * self.coin_amount_long
                self.growth_percentage_from_entry_price = 100 * delta_price / self.entry_price
            
            else:
                self.value                              = self.coin_amount_borrowed_to_enter_short * self.price
                self.growth_usd                         = self.fiat_amount_received_to_sell_and_enter_short - self.coin_amount_borrowed_to_enter_short * self.price
                self.growth_percentage_from_entry_price = 100 * self.growth_usd / self.entry_price

        
        except:
            tk.create_new_notification("runtime error", format_exc())




