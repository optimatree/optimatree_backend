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
        return JsonResponse({'message': 'invalid request'})
    def put(self, request, *args, **kwargs):
        username = kwargs.get("username")
        fields = json.loads(request.body.decode())
        if username is not None:
            return ProfilesHandler.changeProfileByUsername(username, fields)
        return JsonResponse({'message': 'invalid request'})
