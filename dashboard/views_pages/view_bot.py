import json
from dashboard.views_pages import toolkit as tk
from django.http import HttpResponse
from .context import context_class


                
def get_response(request):

    context = context_class.context_class(request, template='dashboard/bot.html')

    if request.method == "POST":
        if 'req' in request.POST:
            ret = context.handle_ajax_post(request)

            return HttpResponse(json.dumps(ret), content_type='application/json')

        else:
            pass



    return context.response()

