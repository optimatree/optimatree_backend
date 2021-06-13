from django.contrib.auth.models import User
import re
    
def IsValidUsername(username):
    # A regex expression mapping the string to alphanumeric username 
    # with the exception of '_' and '-'.
    return re.fullmatch("^[A-Za-z0-9_-]+$", username) and len(username) > 1

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
    return re.fullmatch("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email)
