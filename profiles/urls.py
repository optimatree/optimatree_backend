from django.urls import path, include
from .views import *
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
urlpatterns = [
    path('username/<username>', csrf_exempt(ProfileByUsername().HandleRequest)),
]