from django.http import HttpResponse
from django.template import loader
import json
from . import ajax_posts
from django.http import HttpResponse, HttpResponseRedirect


class context_class():
    def __init__(self, request, template):
        self.request = request
        self.template = template


        self.dict = {'path': self.request.path}

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

        if self.request.method == "POST":

            return HttpResponseRedirect(self.request.path)

        else:

            return HttpResponse(template.render(self.dict, self.request))


