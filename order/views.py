import json
import string
import random

from .models    import Order
from user.utils import login_required

from django.views import View
from django.http  import HttpResponse, JsonResponse
from django.db    import IntegrityError

class OrderView(View):
    @login_required
    def post(self, request):
        user       = request.user
        order_data = json.loads(request.body)

        try:
            Order.objects.create(
                user         = user,
                order_number = ''.join(random.choice(string.ascii_uppercase + string.digits)
                                       for x in range(12)),
                product      = order_data['product'],
                payment_date = order_data['payment_date']
            )

            return HttpResponse(status = 201)

        except IntegrityError:
            return JsonResponse({"error" : "DUPLICATE_ORDER_NUMBER"}, status = 409)

        except KeyError:
            return JsonResponse({"error" : "INVALID_KEYS"}, status = 400)
