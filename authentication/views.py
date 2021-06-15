from utils import response
from profiles.ProfilesHandler import ProfilesHandler
from utils.helper import *
def login(request, *args, **kwargs):
    return response.failure

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
    user = User.objects.get(username=username)
    user.delete()
    return response.succes
