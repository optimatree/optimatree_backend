from django.views.decorators.csrf import csrf_exempt
from utils import response


class RequestHandler:
    @csrf_exempt
    def handle_request(self, request, *args, **kwargs):
        if request.method == "GET":
            return self.get(request, *args, **kwargs)
        elif request.method == "POST":
            return self.post(request, *args, **kwargs)
        elif request.method == "PUT":
            return self.put(request, *args, **kwargs)
        elif request.method == "DELETE":
            return self.delete(request, *args, **kwargs)
        else:
            return response.sendstatus("Invalid Method")
    
    def get(self, request, *args, **kwargs):
        return response.sendstatus("Not a GET Method")
    
    def post(self, request, *args, **kwargs):
        return response.sendstatus("Not a POST Method")

    def put(self, request, *args, **kwargs):
        return response.sendstatus("Not a PUT Method")
    
    def delete(self, request, *args, **kwargs):
        return response.sendstatus("Not a DELETE Method")
