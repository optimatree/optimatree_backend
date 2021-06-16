from utils import response
from utils.RequestHandler import RequestHandler
from django.contrib.auth.models import User
from django.http.response import JsonResponse
import json
from profiles.ProfilesHandler import ProfilesHandler

class ProfileByUsername(RequestHandler):
    def get(self, request, *args, **kwargs):
        username = kwargs.get("username")
        
        if username is not None:
            return ProfilesHandler.getUserProfileByUsername(username)
        
        return response.invalid_data
    
    def put(self, request, *args, **kwargs):
        username = kwargs.get("username")
        fields = json.loads(request.body.decode())
        
        if username is not None:
            return ProfilesHandler.changeProfileByUsername(username, fields)
        
        return response.invalid_data
