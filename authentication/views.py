from django.http.response import JsonResponse

def login(request, *args, **kwargs):

    return JsonResponse({
        "msg": "Hello, world!"
    })

def signup(request, *args, **kwargs):

    return JsonResponse(
        {
            "Status": "Signup Success"
        }
    )