import json
from json.decoder import JSONDecodeError
from utils.decorators import HandleError, delete, get, post, unauthorized_get, unauthorized_post
from utils import response
from profiles.ProfilesHandler import ProfilesHandler
from utils.auth_helper import *

@unauthorized_post
def signin(request, *args, **kwargs):
    query = json.loads(request.body)    
    username = query.get("username")
    password = query.get("password")

    if not request.is_authenticated:
        user = authenticate(request, username=username, password=password)
        if user is not None:
            token = login(user)

            if token is not None:
                return response.sendstatus({
                    'access_token': token.token,
                    'refresh_token': token.refresh_token,
                    'expires': token.expires,
                })
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
    query = json.loads(request.body)
    email = query.get("email")
    first_name = query.get("first_name")
    last_name = query.get("last_name")
    username = query.get("username")
    password = query.get("password")

    return ProfilesHandler.createuser(username, email, password, first_name, last_name)

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
