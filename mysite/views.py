import json
from django.shortcuts import redirect
from django.template import loader

from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
from mysite.forms import AuthBasicForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse

from dashboard.views_pages import toolkit as tk
from django.contrib.auth.decorators import login_required
import requests
from django.views.decorators.http import require_http_methods
from dashboard.views_pages.pulse_handler import handle_a_pulse
from dashboard.views_pages.depth_handler import handle_a_depth_pulse
from dashboard.views_pages import view_depth
from dashboard.views_pages import view_orders
from dashboard.views_pages import view_manual

from dashboard.views_pages import view_pairs
from dashboard.views_pages import view_pair
from dashboard.views_pages import view_bot
from dashboard.views_pages import view_dex

@never_cache
@csrf_exempt
@login_required(login_url='login', redirect_field_name=None)
def index(request):
    return redirect(tk.redirect_to_dashboard)


@never_cache
@csrf_exempt
def logout_view(request):
    logout(request)
    return redirect(tk.redirect_to_login)



def verify_turnstile_token(request):

    try:
        token = request.POST['cf-turnstile-response']
        response = requests.post(
            'https://challenges.cloudflare.com/turnstile/v0/siteverify',
            data={
                'secret': '0x4AAAAAABy0ao_nOZzkOhRY_srk_5EEqSI',
                'response': token
            }
        )
        result = response.json()
        return result.get('success', False)
    except requests.RequestException as e:
        return False



@never_cache
@csrf_exempt
def login_view(request):

    if request.user.is_authenticated:

        return redirect(tk.redirect_to_dashboard)


    form = AuthBasicForm()

    if request.method == 'POST':

        form = AuthBasicForm(request.POST)

        if verify_turnstile_token(request):

            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:

                login(request, user=user)

                return redirect(tk.redirect_to_dashboard)

    context = {'form': form}

    template = loader.get_template('dashboard/login.html')

    return HttpResponse(template.render(context, request))



@never_cache
@csrf_exempt
@login_required(login_url='login', redirect_field_name=None)
def global_view(request):
    
    if request.method == "POST":

        originating_path = request.POST['originating_path']


        # if 'unblock_pulses' in request.POST:
        #     tk.update_admin_settings("pulses_are_being_blocked", False)

        # elif 'block_pulses' in request.POST:
        #     tk.update_admin_settings("pulses_are_being_blocked", True)

        if 'admin_settings_interval' in request.POST:
            tk.update_admin_settings("interval", int(request.POST['admin_settings_interval']))

        elif 'admin_settings_tx_tries' in request.POST:
            tk.update_admin_settings("tx_tries", int(request.POST['admin_settings_tx_tries']))

        elif 'admin_settings_fiat_coin' in request.POST:
            tk.update_admin_settings("fiat_coin", request.POST['admin_settings_fiat_coin'])

        elif 'admin_settings_secure_profit_ratio' in request.POST:
            tk.update_admin_settings("secure_profit_ratio", eval(request.POST['admin_settings_secure_profit_ratio']))

        elif 'admin_settings_gas_speed' in request.POST:
            tk.update_admin_settings("gas_speed", request.POST['admin_settings_gas_speed'])

        elif 'active_account__select' in request.POST:
            tk.update_admin_settings("active_account", request.POST['active_account__select'])

            from dashboard.views_pages.context.ajax.ajax_posts import update_balances
            update_balances()

        return redirect(originating_path)



@never_cache
@csrf_exempt
@login_required(login_url='login', redirect_field_name=None)
def depth_view(request):
    return view_depth.get_response(request)


@never_cache
@csrf_exempt
@login_required(login_url='login', redirect_field_name=None)
def bot_view(request):
    return view_bot.get_response(request)

@never_cache
@csrf_exempt
@login_required(login_url='login', redirect_field_name=None)
def dex_view(request):
    return view_dex.get_response(request)


@never_cache
@csrf_exempt
@login_required(login_url='login', redirect_field_name=None)
def orders_view(request):
    return view_orders.get_response(request)

@never_cache
@csrf_exempt
@login_required(login_url='login', redirect_field_name=None)
def manual_view(request):
    return view_manual.get_response(request)



@never_cache
@csrf_exempt
@login_required(login_url='login', redirect_field_name=None)
def pairs_view(request):
    return view_pairs.get_response(request)


    
@never_cache
@csrf_exempt
@login_required(login_url='login', redirect_field_name=None)
def pair_view(request, pair_uuid):
    return view_pair.get_response(request, pair_uuid)


    

@never_cache
@csrf_exempt
@require_http_methods(["POST"])
def api_pulse_view(request):
    ret = handle_a_pulse(request)
    return HttpResponse(json.dumps(ret))
    


@never_cache
@csrf_exempt
@require_http_methods(["POST"])
def api_depth_view(request):
    handle_a_depth_pulse(request)
    return HttpResponse(json.dumps({}))
    

