from django.urls import path, include
from .views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('login/', csrf_exempt(login)),
    path('signup/', csrf_exempt(signup)),
    path('checkusername/', csrf_exempt(checkusername)),
    path('checkemailid/', csrf_exempt(checkemailid))
]