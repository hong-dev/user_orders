import json

from .models     import Order
from user.models import User
from user.utils  import login_required, random_number_generator

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
                order_number = random_number_generator(),
                product      = order_data['product'],
                payment_date = order_data['payment_date']
            )

            return HttpResponse(status = 201)

        except IntegrityError:
            return JsonResponse({"error" : "DUPLICATE_ORDER_NUMBER"}, status = 409)

        except KeyError:
            return JsonResponse({"error" : "INVALID_KEYS"}, status = 400)

class OrderDetailView(View):
    def get(self, request):
        user_id = request.GET.get('user')

        order_list = (
            Order
            .objects
            .select_related('user')
            .filter(user = user_id)
            .order_by('-payment_date')
        )

        orders = [
            {
                "id"           : order.id,
                "order_number" : order.order_number,
                "product"      : order.product,
                "payment_date" : order.payment_date
            } for order in order_list ]

        return JsonResponse({"orders" : orders}, status = 200)

class OrderListView(View):
    def get(self, request):
        limit  = int(request.GET.get('limit', 10))
        offset = int(request.GET.get('page', 0)) * limit
        name   = request.GET.get('name')
        email  = request.GET.get('email')

        order_list = (
            Order
            .objects
            .select_related('user')
        )

        users = User.objects.exclude(order = None)

        if name:
            users = users.filter(name__icontains = name)
        elif email:
            users = users.filter(email__icontains = email)

        orders = [
            {
                "id"           : order.id,
                "user_id"      : order.user.id,
                "user_name"    : order.user.name,
                "user_email"   : order.user.email,
                "order_number" : order.order_number,
                "product"      : order.product,
                "payment_date" : order.payment_date
            }
            for user in users if
            (order := order_list.filter(user = user.id).latest('payment_date'))
        ]

        if len(orders):
            orders = orders[offset : offset + limit]

            return JsonResponse({"orders" : orders}, status = 200)

        return JsonResponse({"error" : "ORDER_DOES_NOT_EXIST"}, status = 400)
