import json
from dashboard.views_pages import toolkit as tk
from django.http import HttpResponse
from .context import context_class
                
def get_response(request):

    context = context_class.context_class(request, template='dashboard/depth.html')

    if request.method == "POST":
        if 'req' in request.POST:
            ret = context.handle_ajax_post(request)

            return HttpResponse(json.dumps(ret), content_type='application/json')


        else:

            if 'update_depth_plot_settings' in request.POST:
                admin_settings = tk.get_admin_settings()

                admin_settings.depth_lowest_price = float(request.POST['depth_lowest_price'])
                admin_settings.depth_highest_price = float(request.POST['depth_highest_price'])
                admin_settings.depth_cluster_width_usd = float(request.POST['depth_cluster_width_usd'])
                admin_settings.depth_filtering_active = 'depth_filtering_active' in request.POST


                admin_settings.save()


    context.dict['admin_settings'] =  tk.get_admin_settings()

    return context.response()

