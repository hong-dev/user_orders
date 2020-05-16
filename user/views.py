import json
import bcrypt
import jwt

from project.settings import SECRET_KEY, ALGORITHM
from .models          import Gender, User

from django.views import View
from django.http  import HttpResponse, JsonResponse

class SignUpView(View):
    def post(self, request):
        user_data = json.loads(request.body)

        gender = user_data.get('gender')

        try:
            if User.objects.filter(email = user_data['email']).exists():
                return JsonResponse({"error" : "EMAIL_ALREADY_EXISTS"}, status = 400)

            User.objects.create(
                name         = user_data['name'],
                nickname     = user_data['nickname'],
                password     = bcrypt.hashpw(
                    user_data['password'].encode('utf-8'),
                    bcrypt.gensalt()
                ).decode('utf-8'),
                phone_number = user_data['phone_number'],
                email        = user_data['email'],
                gender       = Gender.objects.get(gender = gender) if gender else None
            )

            return HttpResponse(status = 200)

        except KeyError:
            return JsonResponse({"error" : "INVALID_KEYS"}, status = 400)

        except Gender.DoesNotExist:
            return JsonResponse({"error" : "GENDER_DOES_NOT_EXIST"}, status = 400)

class SignInView(View):
    def post(self, request):
        user_data = json.loads(request.body)

        try:
            if User.objects.filter(email = user_data['email']).exists():
                user = User.objects.get(email = user_data['email'])

                if bcrypt.checkpw(
                    user_data['password'].encode('utf-8'),
                    user.password.encode('utf-8')
                ):
                    token = jwt.encode({'email' : user.email},
                                       SECRET_KEY,
                                       algorithm = ALGORITHM
                                      ).decode('utf-8')

                    return JsonResponse({"token" : token}, status = 200)

                return JsonResponse({"error" : "WRONG_PASSWORD"}, status = 401)

            return JsonResponse({"error" : "USER_DOES_NOT_EXIST"}, status = 400)

        except KeyError:
            return JsonResponse({"error" : "INVALID_KEYS"}, status = 400)
