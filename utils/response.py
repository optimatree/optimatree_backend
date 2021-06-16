from django.http.response import JsonResponse

success = JsonResponse({ "msg": "success" })
failure = JsonResponse({ "msg": "failure" }, status=400)
server_error = JsonResponse({ "msg": "Internal Server Error" }, status=500)
invalid_data = JsonResponse({ "msg": "Invalid Data" }, status=400)
invalid_method = JsonResponse({ "msg": "Invalid Method" }, status=400)
unauthorized_request = JsonResponse({ "msg": "Unauthorized Request" }, status=400)

def sendstatus(status_msg, status=200):
    return JsonResponse({"msg": status_msg}, status=status)