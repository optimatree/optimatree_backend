from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404
from api.views import page_not_found
from django_email_verification import urls as email_urls

handler404 = page_not_found

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path("404/", page_not_found),
    path('email/', include(email_urls)),
]