import json
from profiles.models import Profile
from django.contrib.auth.models import User
from django.http.response import JsonResponse
from django.forms.models import model_to_dict
<<<<<<< HEAD
from utils.auth_helper import *
=======
from utils.helper import *
from django_email_verification import send_email

>>>>>>> 0724ebdaa4ecb5804930f6afae9cc2ef1d8ec6fd

class ProfilesHandler:
    restricted_fields = ['username', 'email', 'first_name', 'last_name']
    @staticmethod
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
        profile = Profile(user=user, bio="Hey there!")
        user.is_active = False
        send_email(user)
        user.save()
        profile.save()
        return response.success

    @staticmethod
    def getProfileInfo(user, unrestricted=False):
        if user is None:
            return { 'msg': "User is not Found" }
        profile_info = model_to_dict(user.profile)
        if unrestricted is True:
            user_info = model_to_dict(user)
        else:
            user_info = model_to_dict(user, fields=ProfilesHandler.restricted_fields)

        profile_info['user'] = user_info
        
        return profile_info

    @staticmethod
    def getUserProfileByUsername(username, unrestricted=False):
        user = User.objects.get(username=username)
        user_info = ProfilesHandler.getProfileInfo(user, unrestricted)
        return JsonResponse({'user_info': user_info})
    
    @staticmethod
    def getUserProfileByEmailID(email, unrestricted=False):
        user = User.objects.get(email=email)
        user_info = ProfilesHandler.getProfileInfo(user, unrestricted)
        return JsonResponse({'user_info': user_info})
    
    @staticmethod
    def getUserProfileByUserID(user_id, unrestricted=False):
        user = User.objects.get(id=user_id)
        user_info = ProfilesHandler.getProfileInfo(user, unrestricted)
        return JsonResponse({'user_info': user_info})

    @staticmethod
    def changeProfileByUsername(username, fields):
        user = User.objects.filter(username=username).first()
        result = dict()
        for key in ProfilesHandler.restricted_fields:
            result[key] = fields[key]
        user.from_dict(result)
        user.save()
        return response.success

    @staticmethod
    def getAllUsersRestrictedInfo():
        result = []
        profiles = list(Profile.objects.values())
        for profile in profiles:
            user = User.objects.filter(id=profile['user_id']).first()
            user_info = ProfilesHandler.getProfileInfo(user)
            user_info['bio'] = profile['bio']
            result.append(user_info)
        return JsonResponse({'profiles': result})
    
    @staticmethod
    def getAllUsersUnrestrictedInfo():
        result = []
        profiles = list(Profile.objects.values())
        for profile in profiles:
            user = User.objects.filter(id=profile['user_id']).first()
            user_info = ProfilesHandler.getProfileInfo(user)
            result.append(user_info)
        return JsonResponse({'profiles': result})
