from django.http import HttpResponse
from django.template import loader
import json
from dashboard.views_pages.context.ajax import ajax_posts
from django.http import HttpResponse, HttpResponseRedirect
from mysite import settings
from dashboard.views_pages import toolkit as tk
from dashboard.models import models_transaction
from dashboard.models import models_adminsettings
from dashboard.models import models_order
from dashboard.models import models_position

class context_class():
    def __init__(self, request, template):
        self.request = request
        self.template = template


        self.dict = {
            'path': self.request.path,
            'DEBUG': settings.DEBUG

            }

        if request.user.is_authenticated:

            self.dict['user'] = json.dumps({
                })





    def handle_ajax_post(self, request):
        """
        all post made by ajax are handled here
        this is to keep the actual view file clean
        ajax post do not effect the html response

        """
        return ajax_posts.handle_ajax_posts(self, request)


    def error(self, error):
        self.dict['error'] = error

    def success(self, success_msg):
        self.dict['success'] = success_msg


    def response(self):

        template = loader.get_template(self.template)

        self.dict['admin_settings'] = tk.get_admin_settings()
        self.dict['coins'] =  models_transaction.coins
        self.dict['fiat_coins'] =  models_transaction.fiat_coins
        self.dict['gas_speeds'] =  models_adminsettings.gas_speeds
        self.dict['auto_exit_styles'] =  models_order.auto_exit_styles

        self.dict['new_random_name'] =  tk.get_new_random_name()


        # stats:
        all_positions = models_position.Position.objects.all()
        all_positions_active = models_position.Position.objects.filter(active = True)

        total_fiat_from_shorts = round(sum([x.fiat_amount_received_to_sell_and_enter_short for x in all_positions_active if not x.is_long]), 2)

        total_profit = round(sum([x.final_profit_usd for x in all_positions]), 2)

        self.dict['stats'] = {
            'total_profit' : total_profit,
            'total_fiat_from_shorts' : total_fiat_from_shorts,
        }



        if self.request.method == "POST":

            return HttpResponseRedirect(self.request.path)

        else:

            return HttpResponse(template.render(self.dict, self.request))


