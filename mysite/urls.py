
"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from . import views


urlpatterns = [


    path('', views.index, name='mainindex'),

    path('logout/',     views.logout_view,   name='logout'),
    path('login/',      views.login_view,      name='login'),

    path('api_pulse/',      views.api_pulse_view,      name='api_pulse'),
    path('api_depth/',      views.api_depth_view,      name='api_depth'),

    path('dashboard/', include('dashboard.urls')),
    
    path('orders/',                     views.orders_view,      name='orders'),

    path('pairs/',                      views.pairs_view,       name='pairs'),
    path('pair/<str:pair_uuid>/',       views.pair_view,        name='pair'),
    
    path('manual/',                     views.manual_view,      name='manual'),
    path('depth/',                      views.depth_view,       name='depth'),
    path('bot/',                        views.bot_view,         name='bot'),

    path('global/',                     views.global_view,      name='global'),

    path('admin34k5jh34KJSHDF345kjh2234sdf/', admin.site.urls),


    path('', include('django.contrib.auth.urls')), # this includes /login /logout /password_change /password_reset

]

