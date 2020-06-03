import jwt
import re
import string
import random

from .models          import User
from project.settings import SECRET_KEY, ALGORITHM

from django.http            import JsonResponse
from django.core.validators import validate_email, validate_integer
from django.core.exceptions import ValidationError
from django.core.cache      import cache

def login_required(function):
    def wrapper(self, request, *args, **kwargs):
        token = request.headers.get('Authorization', None)

        if token:
            try:
                token_cache   = cache.get(token)
                decode        = jwt.decode(token_cache, SECRET_KEY, algorithm = ALGORITHM)
                user          = User.objects.get(email = decode['email'])

                request.user  = user
                request.token = token

            except jwt.DecodeError:
                return JsonResponse({"error" : "INVALID_TOKEN"}, status = 400)

            except User.DoesNotExist:
                return JsonResponse({"error" : "INVALID_USER"}, status = 401)

            return function(self, request, *args, **kwargs)

        return JsonResponse({"error" : "LOGIN_REQUIRED"}, status = 401)

    return wrapper

def input_validator(user_data):
    try:
        validate_email(user_data['email'])
        validate_integer(user_data['phone_number'])

        if not user_data['name'].isalpha():
            return JsonResponse({"error" : "INVALID_NAME"}, status = 400)

        user_data['nickname'].encode(encoding='ascii')

        if not (user_data['nickname'].isalpha() and user_data['nickname'].islower()):
            return JsonResponse({"error" : "INVALID_NICKNAME"}, status = 400)

        if not re.match(
            r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*()_])[A-Za-z\d!@#$%^&*()_]{10,}',
            user_data['password']
        ):
            return JsonResponse({"error" : "INVALID_PASSWORD"}, status = 400)

    except UnicodeEncodeError:
        return JsonResponse({"error" : "INVALID_NICKNAME"}, status = 400)

    except ValidationError:
        return JsonResponse({"error" : "INVALID_TYPE"}, status = 400)

    except KeyError:
        return JsonResponse({"error" : "INVALID_KEYS"}, status = 400)

def random_number_generator():
    return ''.join(random.choice(string.ascii_uppercase + string.digits)
                   for x in range(12))
