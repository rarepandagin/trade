from traceback import format_exc
from dashboard.views_pages import toolkit as tk
import json
from dashboard.models import models_tick



def get_clustered_prices(price_volume_pairs, lowest_price, highest_price, cluster_width_usd):
    ret = []

    i =0 
    n = int((highest_price - lowest_price) / cluster_width_usd)
    n = max(1, n)

    for i in range(n):
        start_price = lowest_price + i * cluster_width_usd
        end_price = start_price + cluster_width_usd
        
        cluster = [x for x in price_volume_pairs if start_price <= x[0] < end_price]


        cluster_vol_sum = sum([x[1] for x in cluster]) 

        if cluster_vol_sum > 0:
            cluster_price = sum([x[0] * x[1] for x in cluster]) / cluster_vol_sum

            ret.append([cluster_price, cluster_vol_sum])

    return ret



def handle_a_depth_pulse(request):

        try:
            payload = json.loads(request.body.decode('utf-8'))
        except:
            return

        if payload.get('key', '') != 'XiKd2uXZuT5vBU5mr2Qi':
            return 

        else:

            try:
                admin_settings = tk.get_admin_settings()

                if admin_settings.depth_filtering_active:
                    bids = get_clustered_prices(payload['bids'], admin_settings.depth_lowest_price, admin_settings.depth_highest_price, admin_settings.depth_cluster_width_usd)
                    asks = get_clustered_prices(payload['asks'], admin_settings.depth_lowest_price, admin_settings.depth_highest_price, admin_settings.depth_cluster_width_usd)
                else:
                    bids = payload['bids']
                    asks = payload['asks']

                if len(bids) == 0 or len(asks)==0:
                    return
                    
                best_bid_price =    bids[-1][0]
                best_bid_volume =   bids[-1][1]
                best_ask_price =    asks[0][0]
                best_ask_volume =   asks[0][1]


                models_tick.Tick(
                    data={
                        'best_bid_price': best_bid_price,
                        'best_ask_price': best_ask_price,
                        'best_bid_volume': best_bid_volume,
                        'best_ask_volume': best_ask_volume,
                        'price': admin_settings.prices['weth']
                        }
                ).save()

                tick_to_keep = models_tick.Tick.objects.all().order_by('-epoch')[:250] 

                models_tick.Tick.objects.exclude(pk__in=tick_to_keep).delete()   

                
                
                mean_price = (best_bid_volume * best_bid_price + best_ask_volume * best_ask_price) / (best_bid_volume + best_ask_volume)



                payload =  {
                        
                        "bids": bids,
                        "asks": asks,

                        "mean_price": mean_price,

                        "best_bid_price": best_bid_price,
                        "best_ask_price": best_ask_price,

                        "best_bid_volume": best_bid_volume,
                        "best_ask_volume": best_ask_volume,

                        "admin_settings": tk.serialize_object(admin_settings),

                        "ticks": [tk.serialize_object(x) for x in models_tick.Tick.objects.all().order_by('epoch')],
                    }

                tk.send_message_to_frontend_depth(topic='update_depth_chart', payload=payload)

            except:

                tk.logger.info(format_exc())
                return 
