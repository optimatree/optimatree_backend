import json
from json.decoder import JSONDecodeError
from utils.RequestHandler import RequestHandler
from utils.decorators import HandleError, delete, get, post, unauthorized_get, unauthorized_post
from django.http.response import JsonResponse
from utils import response
from profiles.ProfilesHandler import ProfilesHandler
from utils.auth_helper import *
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import send_mail, BadHeaderError

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
def signup(request, *args, **kwargs):
    if not request.is_authenticated:
        query = request.POST
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

@post
def change_password(request, *args, **kwargs):
    query = json.loads(request.body)
    if UsernameExists(query.get("username")) is False:
        return response.sendstatus('Username does not exist')
    
    username = query.get("username")
    old_password = query.get("old_password")
    new_password = query.get("new_password")
    
    if old_password is None:
        return response.sendstatus('Invalid request')
    
    user = User.objects.get(username=username)

    if user.check_password(old_password):
        user.set_password(new_password)
        user.save()
        return response.success
    
    return response.sendstatus('Wrong password')

@unauthorized_post
def reset_password(request, *args, **kwargs):
    query = json.loads(request.body)
    
    reset_token = query.get("reset_token")
    new_password = query.get("new_password")

    if new_password is None or reset_token is None:
        return response.sendstatus('Invalid request')
    
    user = getuserfromresettoken(reset_token)

    if user is not None:
        user.set_password(new_password)
        user.save()
        return response.success
    
    return response.sendstatus('Invalid Request')

@unauthorized_post
@HandleError(exception=(BadHeaderError), msg="Invalid Request")
def initiate_password_reset(request, *args, **kwargs):
    email = request.POST.get("email")
    user = User.objects.get(email=email)

    subject = "Password Reset Requested"
    email_template_name = "password_reset_email.txt"
    c = {
    "email":user.email,
    'domain':'127.0.0.1:8000',
    'site_name': 'OptimaTree',
    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
    "user": user,
    'token': default_token_generator.make_token(user),
    'protocol': 'http',
    }
    email = render_to_string(email_template_name, c)
    send_mail(subject, email, 'optimatree@gmail.com' , [user.email], fail_silently=False)
    return JsonResponse({'msg':'Success'})
