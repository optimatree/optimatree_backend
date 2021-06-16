from django.urls import path, include
from .views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('signin/', signin),
    path('signout/', signout),
    path('signup/', signup),
    path('checkusername/', checkusername),
    path('checkemailid/', checkemailid),
    path('deleteuser/', deleteuser),
    path('checkuser/', check_user)
]