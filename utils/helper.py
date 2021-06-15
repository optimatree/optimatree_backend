from django.contrib.auth.models import User
from utils import response
import re
    
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

def createuser(username, email, password, first_name, last_name):
    if isEmailValid(email) is False:
        return response.sendstatus("Email format invalid")
    
    if EmailExists(email):
        return response.sendstatus("Email Already Exists!")

    if IsValidUsername(username) is False:
        return response.sendstatus("Username format invalid!")

    if UsernameExists(username):
        return response.sendstatus("Username Already Exists!")

    if ValidatePassword(password) is False:
        return response.sendstatus("Enter a Valid Password!")
    
    user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
    user.save()
    print(user.is_authenticated)
    return response.success

# Functions for Authentication Checking
def check_auth(token):
    return (token == "hello")