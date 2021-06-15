from django.urls import path, include
from .views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('signin/', csrf_exempt(signin)),
    path('signout/', csrf_exempt(signout)),
    path('signup/', csrf_exempt(signup)),
    path('checkusername/', csrf_exempt(checkusername)),
    path('checkemailid/', csrf_exempt(checkemailid)),
    path('deleteuser/', csrf_exempt(deleteuser))
]