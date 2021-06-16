from django.urls import path, include
from .views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('signin/', signin),
    path('signout/', signout),
    path('signup/', csrf_exempt(signup)),
    path('checkusername/', checkusername),
    path('checkemailid/', checkemailid),
    path('deleteuser/', deleteuser),
    path('tokenrefresh/', TokenRefresh().handle_request),
    path('change_password/', change_password),
    path('checkuser/', check_user),
    path('initiate_password_reset/', initiate_password_reset)
]