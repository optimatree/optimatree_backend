from utils.helper import check_auth


def AuthMiddleware(get_response):
    def middleware(request, *args, **kwargs):
        request.is_authenticated = False
        header = request.headers.get("Authorization")
        if header:
            token = header.split(" ")[1]
            if check_auth(token):
                request.is_authenticated = True

        response = get_response(request, *args, **kwargs)

        return response

    return middleware