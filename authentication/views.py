from django.http.response import JsonResponse
from utils import response
from profiles.ProfilesHandler import ProfilesHandler
from utils.helper import *
from django.contrib.auth import authenticate, login, logout
def signin(request, *args, **kwargs):
    query = request.POST
    username = query.get(key="username")
    password = query.get(key="password")
    print(username, password)
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
    else:
        return response.sendstatus('Not Authenticated')
    return response.sendstatus('User Authenticated')

def signout(request, *args, **kwargs):
    logout(request)
    return response.sendstatus("Sign out successful")

def signup(request, *args, **kwargs):
    query = request.POST
    email = query.get(key="email")
    first_name = query.get(key="first_name")
    last_name = query.get(key="last_name")
    username = query.get(key="username")
    password = query.get(key="password")
    return ProfilesHandler.createuser(username, email, password, first_name, last_name)

def checkemailid(request, *args, **kwargs):
    if EmailExists(request.GET.get(key="email")):
        return response.success
    return response.sendstatus('EmailID does not exist')

def checkusername(request, *args, **kwargs):
    if UsernameExists(request.GET.get(key="username")):
        return response.success
    return response.sendstatus('Username does not exist')

def deleteuser(request, *args, **kwargs):
    if UsernameExists(request.POST.get(key="username")) is False:
        return response.sendstatus('Username does not exist')
    username = request.POST.get(key="username")
    password = request.POST.get(key="password")
    if password is None:
        return response.sendstatus('Invalid request')
    user = User.objects.get(username=username)
    if user.check_password(password):
        user.delete()
        return response.success
    return response.sendstatus('Wrong password')

def check_user(request, *args, **kwargs):
    if UsernameExists(request.POST.get(key="username")) is False:
        return response.sendstatus('Username does not exist')
    username = request.POST.get(key="username")
    user = User.objects.get(username=username)
    return JsonResponse({'User Status':user.is_active})