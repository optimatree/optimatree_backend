import re

from authentication.models import AuthToken
from utils import response
from django.contrib.auth.models import AnonymousUser, User
from django.contrib.auth.hashers import check_password
from django.http import HttpRequest
    
def IsValidUsername(username):
    # A regex expression mapping the string to alphanumeric username 
    # with the exception of '_' and '-'.
    return bool(re.fullmatch("^[A-Za-z0-9_-]+$", username) and len(username) > 1)

def UsernameExists(username):
    if User.objects.filter(username=username).exists():
        return True
    return False

def ValidatePassword(password):
    return len(password) > 7

def EmailExists(email):
    if User.objects.filter(email=email).exists():
        return True
    return False

def isEmailValid(email):
    return bool(re.fullmatch("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email))

# Authentication Operations
def authenticate(request: HttpRequest, username: str, password: str):
    if request.is_authenticated:
        return request.user
    
    users = User.objects.filter(username=username)
    
    if len(users) > 0:
        user = users.first()
        if(check_password(password=password, encoded=user.password)):
            return user

def login(user: User):
    if user is not None:
        tokens = AuthToken.objects.filter(user=user)
        
        t = None
        
        if len(tokens) > 0:
            t = tokens.first()
            t.delete()

        t = AuthToken(user=user)
        t.save()

        return t

    return None

def logout(request: HttpRequest):
    if (request.is_authenticated) and isinstance(request.user, User):
        t = get_token_by_user(request.user)
        if t is not None:
            t.revoke()
            return True

    return False

def get_token(token: str):
    if len(token) == AuthToken.token_length:
        t = AuthToken.objects.filter(token=token)
        if len(t) > 0:
            t = t.first()
            if not t.is_expired():
                return t
            
            t.revoke()

    return None

def get_token_by_user(user: User) -> AuthToken:
    if user is not None:
        t = AuthToken.objects.filter(user=user)
        if len(t) > 0:
            t = t.first()
            if not t.is_expired():
                return t
            t.revoke()

    return None

# Functions for Authentication Checking
def check_auth(token):
    return get_token(token) != None

# Function to Get User by token
def get_user_by_token(token):
    t = get_token(token)
    if t != None:
        return t.user
    
    return AnonymousUser()

def getuserfromresettoken(reset_token):
    pass