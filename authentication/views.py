from authentication import response
from django.http import HttpRequest
from utils.validate import *
from django.contrib.auth.models import User

def login(request, *args, **kwargs):
    return response.failure

def signup(request, *args, **kwargs):
    query = request.POST

    email = query.get(key="email")
    first_name = query.get(key="first_name")
    last_name = query.get(key="last_name")
    username = query.get(key="username")
    password = query.get(key="password")

    if isEmailValid(email) and EmailExists(email):
        return response.sendstatus("Email Already Exists!")
    
    if IsValidUsername(username) and UsernameExists(username):
        return response.sendstatus("Username Already Exists!")

    if ValidatePassword(password) is False:
        return response.sendstatus("Enter a Valid Password!")
    
    user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
    user.save()

    return response.success

def checkemailid(request, *args, **kwargs):
    if EmailExists(request.GET.get(key="email")):
        return response.success
    return response.failure

def checkusername(request, *args, **kwargs):
    if UsernameExists(request.GET.get(key="username")):
        return response.success
    return response.failure

