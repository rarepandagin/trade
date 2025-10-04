from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache

from dashboard.views_pages import view_index

decorators = [never_cache, csrf_exempt, login_required]


@never_cache
@csrf_exempt
@login_required(login_url='login', redirect_field_name=None)

def index(request):
    return view_index.get_response(request)









