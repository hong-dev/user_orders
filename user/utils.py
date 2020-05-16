import jwt

from .models          import User
from project.settings import SECRET_KEY, ALGORITHM

from django.http import JsonResponse

def login_required(function):
    def wrapper(self, request, *args, **kwargs):
        token = request.headers.get('Authorization', None)

        if token:
            try:
                decode       = jwt.decode(token, SECRET_KEY, algorithm = ALGORITHM)
                user         = User.objects.get(email = decode['email'])
                request.user = user

            except jwt.DecodeError:
                return JsonResponse({"error" : "INVALID_TOKEN"}, status = 400)

            except User.DoesNotExist:
                return JsonResponse({"error" : "INVALID_USER"}, status = 401)

            return function(self, request, *args, **kwargs)

        return JsonResponse({"error" : "LOGIN_REQUIRED"}, status = 401)

    return wrapper
