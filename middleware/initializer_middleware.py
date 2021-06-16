import traceback

from django.http.response import JsonResponse

class InitializerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request):
        pass

    def process_exception(self, request, exception):
        if exception:
            print(traceback.format_exc())

        return JsonResponse({"msg": "Internal Server Error"}, status=500)