from django.http.response import JsonResponse

def page_not_found(request, *args, **kwargs):
    return JsonResponse({
        'msg': "Route Not Found!"
    }, status=404)