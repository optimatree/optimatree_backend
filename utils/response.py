from django.http.response import JsonResponse

success = JsonResponse({"status": "success"})
failure = JsonResponse({"status": "failure"})

def sendstatus(status_msg):
    return JsonResponse({"status": status_msg})