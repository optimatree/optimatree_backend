from django.http.response import JsonResponse

def login(request, *args, **kwargs):
    print(request.headers)

    return JsonResponse({
        "msg": "Hello, world!"
    })