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
from dashboard.ws_routines.ws_pulse_handler import handle_ws_pulse

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
@require_http_methods(["POST"])

def api_view(request):

    ret = handle_ws_pulse(request)
    return HttpResponse(json.dumps(ret))
