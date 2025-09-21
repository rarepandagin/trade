from django.db import models
from traceback import format_exc
from dashboard.views_pages import toolkit as tk
from dashboard.views_pages import transaction_dispatch

from dashboard.models.coins import *


auto_exit_style_both_ways = "auto_exit_style_both_ways"
auto_exit_style_only_after_profit_take_price_reached = "auto_exit_style_only_after_profit_take_price_reached"
auto_exit_style_only_after_stop_loss_price_reached = "auto_exit_style_only_after_stop_loss_price_reached"
auto_exit_style_never = "auto_exit_style_never"


auto_exit_styles = {
    auto_exit_style_both_ways : "auto_exit_style_both_ways",
    auto_exit_style_only_after_profit_take_price_reached : "auto_exit_style_only_after_profit_take_price_reached",
    auto_exit_style_only_after_stop_loss_price_reached : "auto_exit_style_only_after_stop_loss_price_reached",
    auto_exit_style_never: "auto_exit_style_never",
}

execute_if_price_is_above  = "execute_if_price_is_above"
execute_if_price_is_below  = "execute_if_price_is_below"

entry_conditions = {
    execute_if_price_is_above  : "execute_if_price_is_above",
    execute_if_price_is_below  : "execute_if_price_is_below",
}


short = "short"
long = "long"

position_types = {
    short : "short",
    long : "long",
}



class Order(models.Model):

    id = models.BigAutoField(primary_key=True)

    # initial setup

    name = models.TextField(default="", null=True, blank=True)

    coin = models.CharField(choices=coins, default=weth)

    entry_condition = models.CharField(choices=entry_conditions, default=auto_exit_style_both_ways)

    position_type = models.CharField(choices=position_types, default=long)

    entry_capital = models.FloatField(default=0)


    order_entry_price = models.FloatField(default=0)

    profit_take_price = models.FloatField(default=0)

    stop_loss_price = models.FloatField(default=0)
    
    # if an order is part of a pair, then this property stores the uuid of the pair
    pair_uuid = models.TextField(default="", null=True, blank=True)
    


    # auto
    uuid = models.TextField(default="", null=True, blank=True)
    active = models.BooleanField(default=True)
    executed = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)
    fulfilled = models.BooleanField(default=False)


    # automatic
    epoch_created = models.BigIntegerField(default=0)
    epoch_updated = models.BigIntegerField(default=0)
    epoch_executed = models.BigIntegerField(default=0)


    # settings
    # auto_exit = models.BooleanField(default=False)
    auto_exit_style     = models.CharField(choices=auto_exit_styles,   default=auto_exit_style_only_after_profit_take_price_reached)



    def __str__(self):
        return self.name


    def save(self, *args, **kwargs):
        if self.uuid == '':
            self.uuid = tk.get_new_uuid()
            self.epoch_created = tk.get_epoch_now()

        else:
            self.epoch_updated = tk.get_epoch_now()

        self.order_entry_price                = round(self.order_entry_price, 2)
        self.stop_loss_price            = round(self.stop_loss_price, 2)
        self.profit_take_price      = round(self.profit_take_price, 2)


        super(Order, self).save(*args, **kwargs)



    def execute(self):
        from dashboard.models import models_position
        from dashboard.models import models_transaction
        from dashboard.models import models_pair

        if self.active and (not self.fulfilled):



            """
            the PT price can not be below that the live price for a long
            the PT price can not be higher that the live price for a short
            """

            admin_settings = tk.get_admin_settings()

            live_price = admin_settings.prices[self.coin.lower()]
            
            invalid_profit_take_price = False

            if self.position_type == long and self.profit_take_price <= live_price:
                invalid_profit_take_price = True
            
            if self.position_type == short and self.profit_take_price >= live_price:
                invalid_profit_take_price = True

            if invalid_profit_take_price:

                tk.create_new_notification(title="Buy order deleted", message=f"invalid profit take price for {self.name}")

                self.delete()
                return None


            if self.position_type == long:

                buy_transaction = transaction_dispatch.create_and_actualize_uniswap_fiat_to_token_transaction(self.entry_capital, self.coin)
                buy_transaction.order = self
                buy_transaction.order.save()

                if buy_transaction.state == models_transaction.transaction_state_successful:

                    new_long_position = models_position.Position(
                        order=self,
                        is_long = True,

                        coin_amount_long = buy_transaction.token_amount_received,

                        entry_price=buy_transaction.token_effective_price,

                        profit_take_price = self.profit_take_price,
                        stop_loss_price = self.stop_loss_price,
                        initial_stop_loss_price = self.stop_loss_price,

                    )
                        
                    new_long_position.save()

                    if self.pair_uuid != '':
                        pair = models_pair.Pair.objects.get(uuid=self.pair_uuid)
                        pair.long_position = new_long_position
                        pair.save()


                    self.fulfilled = True
                    tk.create_new_notification(title="Long order fulfilled", message=f"order {self.name} fulfilled")

                else:
                    tk.create_new_notification(title="Long order did not get fulfilled due to tx failure", message=f"tx for order {self.name} failed at execution")
                
                
                buy_transaction.save()



            elif self.position_type == short:


                coin_amount_borrowed_to_enter_short = self.entry_capital / live_price

                borrow_transaction = transaction_dispatch.create_and_actualize_aave_borrow_transaction(borrow_amount=coin_amount_borrowed_to_enter_short)
                borrow_transaction.order = self
                borrow_transaction.save()


                if borrow_transaction.state == models_transaction.transaction_state_successful:
                    tk.create_new_notification(title="Short order borrow was successful", message=f"order name: {self.name}")

                    sell_transaction = transaction_dispatch.create_and_actualize_uniswap_token_to_fiat_transaction(token_to_fiat_amount=coin_amount_borrowed_to_enter_short, coin= self.coin)
                    sell_transaction.order = self
                    sell_transaction.save()

                    if sell_transaction.state == models_transaction.transaction_state_successful:

                        new_short_position = models_position.Position(
                            order=self,
                            is_long = False,

                            coin_amount_borrowed_to_enter_short = coin_amount_borrowed_to_enter_short,
                            fiat_amount_received_to_sell_and_enter_short = sell_transaction.fiat_amount_received,

                            entry_price=sell_transaction.token_effective_price,

                            profit_take_price = self.profit_take_price,
                            stop_loss_price = self.stop_loss_price,
                            initial_stop_loss_price = self.stop_loss_price,
                        )

                        new_short_position.save()


                        if self.pair_uuid != '':
                            pair = models_pair.Pair.objects.get(uuid=self.pair_uuid)
                            pair.short_position = new_short_position
                            pair.save()


                        self.fulfilled = True
                        tk.create_new_notification(title="Short order fulfilled", message=f"order name: {self.name}")

                    else:
                        tk.create_new_notification(title="Short order borrow was successful but the swap tx failed", message=f"tx for order {self.name} failed at execution")
                
                else:
                    tk.create_new_notification(title="Short order borrow failed", message=f"order name: {self.name}")

                    

            self.active = False
            self.executed = True


    def evaluate(self):
        try:
            if self.active and (not self.executed):
    
                admin_settings = tk.get_admin_settings()

                live_price = admin_settings.prices[self.coin.lower()]

                if self.entry_condition == execute_if_price_is_below:
                    if live_price <= self.order_entry_price :
                        self.execute()

                elif self.entry_condition == execute_if_price_is_above:
                    if self.order_entry_price <= live_price :
                        self.execute()  

 

        except:
            tk.create_new_notification("runtime error", format_exc())

        

