from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


class AuthBasicForm(AuthenticationForm):

    class Meta:
        model = User
        fields = []



