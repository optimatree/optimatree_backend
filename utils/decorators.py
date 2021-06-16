from json.decoder import JSONDecodeError
import traceback
from typing import Any, List, Tuple

from django.contrib.auth.models import User
from utils.auth_helper import check_auth

from functools import wraps
from django.http.request import HttpRequest
from utils.helper import print_output
from utils import response

from django.views.decorators.csrf import csrf_exempt

def json_data(function):
    def return_function(request, *args, **kwargs):
        try:
            function(request, *args, **kwargs)
        except JSONDecodeError as e:
            print_output(traceback.format_exc())
            return response.invalid_data
    return return_function

class HandleError:
    def __init__(self, exception, msg: str = "") -> None:
        self.exception = exception
        self.msg = msg

    def __call__(self, function, *args: Any, **kwds: Any) -> Any:
        def return_function(request, *args, **kwargs):
            try:
                return function(request, *args, **kwargs)
            except self.exception as e:
                print_output()
                return response.sendstatus(self.msg)
        
        return return_function


class Request:
    def __init__(self, method: str = "GET") -> None:
        self.method = method

    def __call__(self, function, *args: Any, **kwds: Any) -> Any:

        def return_function(request, *args, **kwargs):
            if request.method == self.method:
                return function(request, *args, **kwargs)
            
            return response.invalid_method
        
        return return_function

class Authorized:
    def __init__(self, method: str = "GET") -> None:
        self.method = method

    def __call__(self, function, *args: Any, **kwds: Any) -> Any:
        
        def return_function(request, *args, **kwargs):
            if request.method == self.method:
                if request is not None and isinstance(request.user, User):
                    return function(request, *args, **kwargs)
                
                return response.unauthorized_request
            
            return response.invalid_method

        return return_function

def get(function):
    
    @csrf_exempt
    @Authorized(method='GET')
    def return_function(request, *args, **kwargs):
        return function(request, *args, **kwargs)

    return return_function

def post(function):
    
    @csrf_exempt
    @Authorized(method='POST')
    def return_function(request, *args, **kwargs):
        return function(request, *args, **kwargs)

    return return_function

def put(function):
    
    @csrf_exempt
    @Authorized(method='PUT')
    def return_function(request, *args, **kwargs):
        return function(request, *args, **kwargs)

    return return_function

def delete(function):
    
    @csrf_exempt
    @Authorized(method='DELETE')
    def return_function(request, *args, **kwargs):
        return function(request, *args, **kwargs)

    return return_function


"""
    Unauthorized Requests
"""
def unauthorized_get(function):
    
    @csrf_exempt
    @Request('GET')
    def return_function(request, *args, **kwargs):
        return function(request, *args, **kwargs)

    return return_function

def unauthorized_post(function):

    @csrf_exempt
    @Request('POST')
    def return_function(request, *args, **kwargs):
        return function(request, *args, **kwargs)

    return return_function

def unauthorized_put(function):
    
    @csrf_exempt
    @Request('PUT')
    def return_function(request, *args, **kwargs):
        return function(request, *args, **kwargs)

    return return_function

def unauthorized_delete(function):

    @csrf_exempt
    @Request('DELETE')
    def return_function(request, *args, **kwargs):
        return function(request, *args, **kwargs)

    return return_function

