import json
from json.decoder import JSONDecodeError
from utils.RequestHandler import RequestHandler
from utils.decorators import HandleError, delete, get, post, unauthorized_get, unauthorized_post
from django.http.response import JsonResponse
from utils import response
from profiles.ProfilesHandler import ProfilesHandler
from utils.auth_helper import *

@unauthorized_post
def signin(request, *args, **kwargs):
    if not request.is_authenticated:
        query = json.loads(request.body)    
        username = query.get("username")
        password = query.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if not user.is_active:
                return response.sendstatus("Please verify your Email")

            token = login(user)

            if token is not None:
                return response.sendstatus(token.to_dict())
        else:
            return response.sendstatus('Not Authenticated')

    return response.sendstatus('User Authenticated')

@unauthorized_get
def signout(request, *args, **kwargs):
    if logout(request):
        return response.sendstatus("Sign out successful")
    else:
        return response.sendstatus("Invalid request")

@unauthorized_post
@HandleError(exception=(TypeError, JSONDecodeError), msg="Invalid Data")
def signup(request, *args, **kwargs):
    if not request.is_authenticated:
        query = json.loads(request.body)
        email = query.get("email")
        first_name = query.get("first_name")
        last_name = query.get("last_name")
        username = query.get("username")
        password = query.get("password")

        return ProfilesHandler.createuser(username, email, password, first_name, last_name)

    return response.sendstatus('User Authenticated')

@unauthorized_get
def checkemailid(request, *args, **kwargs):
    if EmailExists(request.GET.get("email")):
        return response.success
    return response.sendstatus('EmailID does not exist')

@unauthorized_get
def checkusername(request, *args, **kwargs):
    if UsernameExists(request.GET.get("username")):
        return response.success
    return response.sendstatus('Username does not exist')

@delete
def deleteuser(request, *args, **kwargs):
    query = json.loads(request.body)
    if UsernameExists(query.get("username")) is False:
        return response.sendstatus('Username does not exist')
    
    username = query.get("username")
    password = query.get("password")
    
    if password is None:
        return response.sendstatus('Invalid request')
    
    user = User.objects.get(username=username)

    if user.check_password(password):
        user.delete()
        return response.success
    
    return response.sendstatus('Wrong password')

@unauthorized_post
def check_user(request, *args, **kwargs):
    if UsernameExists(request.POST.get(key="username")) is False:
        return response.sendstatus('Username does not exist')
    username = request.POST.get(key="username")
    user = User.objects.get(username=username)
    return JsonResponse({'User Status':user.is_active})

class TokenRefresh(RequestHandler):
    def get(self, request, *args, **kwargs):
        if request.is_authenticated:
            return response.sendstatus(request.user.authtoken.to_dict())
        return response.failure

    @HandleError(exception=JSONDecodeError, msg="Invalid Data")
    def put(self, request, *args, **kwargs):
        data = json.loads(request.body)
        refresh_token = data.get("refresh_token")
        tokens = AuthToken.objects.filter(refresh_token=refresh_token)
        if len(tokens):
            t = tokens.first()
            t.refresh()
            return response.sendstatus(t.to_dict())
        
        return response.sendstatus("Invalid Refresh Token")