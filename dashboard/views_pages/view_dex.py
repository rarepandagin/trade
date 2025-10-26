import json
from dashboard.views_pages import toolkit as tk
from django.http import HttpResponse
from .context import context_class
from dashboard.models import models_token

                
def get_response(request):

    context = context_class.context_class(request, template='dashboard/dex.html')

    if request.method == "POST":
        if 'req' in request.POST:
            ret = context.handle_ajax_post(request)

            json_ret = json.dumps(ret)

            return HttpResponse(json_ret, content_type='application/json')

        else:
            pass

    
    

    return context.response()

