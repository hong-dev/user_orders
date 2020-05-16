import json
import bcrypt
import jwt

from project.settings import SECRET_KEY
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
