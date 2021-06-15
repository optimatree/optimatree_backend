from django.http.response import JsonResponse

success = JsonResponse({"msg": "success"})
failure = JsonResponse({"msg": "failure"})

def sendstatus(status_msg):
    return JsonResponse({"msg": status_msg})