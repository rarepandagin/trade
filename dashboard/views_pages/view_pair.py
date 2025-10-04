import json
from dashboard.views_pages import toolkit as tk
from django.http import HttpResponse
from .context import context_class

from dashboard.models import models_pair

                
def get_response(request, pair_uuid):

    context = context_class.context_class(request, template='dashboard/pair.html')

    pair = models_pair.Pair.objects.get(uuid=pair_uuid)

    if request.method == "POST":
        if 'req' in request.POST:
            ret = context.handle_ajax_post(request)

            return HttpResponse(json.dumps(ret), content_type='application/json')


        else:
            pass


    context.dict['pair'] = pair




    return context.response()

