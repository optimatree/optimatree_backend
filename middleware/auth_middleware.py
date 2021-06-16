from django.contrib.auth.models import User
from authentication.models import AuthToken
from utils.auth_helper import check_auth, get_user_by_token


def AuthMiddleware(get_response):
    def middleware(request, *args, **kwargs):
        request.is_authenticated = False
        token = request.headers.get("Authorization")
        if token:
            request.user = get_user_by_token(token)
            request.is_authenticated = isinstance(request.user, User)

        response = get_response(request, *args, **kwargs)

        return response

    return middleware