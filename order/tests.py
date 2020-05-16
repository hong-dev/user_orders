import json
import bcrypt
import jwt

from .models          import Order
from user.models      import Gender, User
from project.settings import SECRET_KEY, ALGORITHM

from django.test import TestCase, Client

class OrderTest(TestCase):
    def setUp(self):
        Gender.objects.create(
            id     = 1,
            gender = "Woman"
        )

        User.objects.create(
            name         = "홍",
            nickname     = "Dev",
            password     = bcrypt.hashpw("1234".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            phone_number = "01012345678",
            email        = "hong@gamil.com",
            gender       = Gender.objects.get(id = 1)
        )

    def tearDown(self):
        Gender.objects.all().delete()
        User.objects.all().delete()

    def test_order_post_success(self):
        token = jwt.encode(
            {"email" : "hong@gamil.com"},
            SECRET_KEY,
            algorithm = ALGORITHM
        ).decode('utf-8')

        order_data = {
            "product"      : "✅[주말반짝할인]🌙🔮 피니어스 CP 비누💖🐤",
            "payment_date" : "2020-05-17"
        }

        response = Client().post('/order',
                                 json.dumps(order_data),
                                 **{'HTTP_Authorization' : token},
                                 content_type = 'application/json')

        self.assertEqual(response.status_code, 201)

    def test_order_post_payment_key_fail(self):
        token = jwt.encode(
            {"email" : "hong@gamil.com"},
            SECRET_KEY,
            algorithm = ALGORITHM
        ).decode('utf-8')

        order_data = {
            "payment_date" : "2020-05-17"
        }

        response = Client().post('/order',
                                 json.dumps(order_data),
                                 **{'HTTP_Authorization' : token},
                                 content_type = 'application/json')

        self.assertEqual(response.json(),
            {
                "error" : "INVALID_KEYS"
            }
        )
        self.assertEqual(response.status_code, 400)

    def test_order_post_product_key_fail(self):
        token = jwt.encode(
            {"email" : "hong@gamil.com"},
            SECRET_KEY,
            algorithm = ALGORITHM
        ).decode('utf-8')

        order_data = {
            "product" : "✅[주말반짝할인]🌙🔮 피니어스 CP 비누💖🐤"
        }

        response = Client().post('/order',
                                 json.dumps(order_data),
                                 **{'HTTP_Authorization' : token},
                                 content_type = 'application/json')

        self.assertEqual(response.json(),
            {
                "error" : "INVALID_KEYS"
            }
        )
        self.assertEqual(response.status_code, 400)
