import json
import bcrypt
import jwt
import string
import random

from .models          import Order
from user.models      import Gender, User
from project.settings import SECRET_KEY, ALGORITHM

from django.test       import TestCase, Client
from django.core.cache import cache

class OrderTest(TestCase):
    def setUp(self):
        Gender.objects.create(
            id     = 1,
            gender = "Woman"
        )

        User.objects.create(
            id           = 1,
            name         = "홍",
            nickname     = "dev",
            password     = bcrypt.hashpw(
                "1234567aA!".encode('utf-8'),
                bcrypt.gensalt()
            ).decode('utf-8'),
            phone_number = "01012345678",
            email        = "hong@gamil.com",
            gender       = Gender.objects.get(id = 1)
        )

    def tearDown(self):
        Gender.objects.all().delete()
        User.objects.all().delete()

    def test_order_post_success(self):
        user_number = ''.join(random.choice(string.ascii_uppercase + string.digits)
                   for x in range(12))

        token = jwt.encode(
            {"email" : "hong@gamil.com"},
            SECRET_KEY,
            algorithm = ALGORITHM
        ).decode('utf-8')

        cache.get_or_set(user_number, token)

        order_data = {
            "product"      : "✅[주말반짝할인]🌙🔮 피니어스 CP 비누💖🐤",
            "payment_date" : "2020-05-17"
        }

        response = Client().post('/order',
                                 json.dumps(order_data),
                                 **{'HTTP_Authorization' : user_number},
                                 content_type = 'application/json')

        self.assertEqual(response.status_code, 201)

    def test_order_post_payment_key_fail(self):
        user_number = ''.join(random.choice(string.ascii_uppercase + string.digits)
                   for x in range(12))

        token = jwt.encode(
            {"email" : "hong@gamil.com"},
            SECRET_KEY,
            algorithm = ALGORITHM
        ).decode('utf-8')

        cache.get_or_set(user_number, token)

        order_data = {
            "payment_date" : "2020-05-17"
        }

        response = Client().post('/order',
                                 json.dumps(order_data),
                                 **{'HTTP_Authorization' : user_number},
                                 content_type = 'application/json')

        self.assertEqual(response.json(),
            {
                "error" : "INVALID_KEYS"
            }
        )
        self.assertEqual(response.status_code, 400)

    def test_order_post_product_key_fail(self):
        user_number = ''.join(random.choice(string.ascii_uppercase + string.digits)
                   for x in range(12))

        token = jwt.encode(
            {"email" : "hong@gamil.com"},
            SECRET_KEY,
            algorithm = ALGORITHM
        ).decode('utf-8')

        cache.get_or_set(user_number, token)

        order_data = {
            "product" : "✅[주말반짝할인]🌙🔮 피니어스 CP 비누💖🐤"
        }

        response = Client().post('/order',
                                 json.dumps(order_data),
                                 **{'HTTP_Authorization' : user_number},
                                 content_type = 'application/json')

        self.assertEqual(response.json(),
            {
                "error" : "INVALID_KEYS"
            }
        )
        self.assertEqual(response.status_code, 400)

class OrderDetailTest(TestCase):
    def setUp(self):
        Gender.objects.create(
            id     = 1,
            gender = "Woman"
        )

        User.objects.create(
            id           = 1,
            name         = "홍",
            nickname     = "dev",
            password     = "1234567aA!",
            phone_number = "01012345678",
            email        = "hong@gamil.com",
            gender       = Gender.objects.get(id = 1)
        )

        Order.objects.create(
            id           = 1,
            user         = User.objects.get(id = 1),
            order_number = "8UVNSN0Z9IG4",
            product      = "비누",
            payment_date = "2019-03-01T00:24:00"
        )

        Order.objects.create(
            id           = 2,
            user         = User.objects.get(id = 1),
            order_number = "MDT30FXBKY5J",
            product      = "책갈피",
            payment_date = "2020-05-01"
        )

    def tearDown(self):
        Gender.objects.all().delete()
        User.objects.all().delete()
        Order.objects.all().delete()

    def test_order_detail_get_success(self):
        response = Client().get('/order/detail?user=1')

        self.assertEqual(response.json(),
            {
                "orders" : [
                    {
                        "id"           : 2,
                        "order_number" : "MDT30FXBKY5J",
                        "product"      : "책갈피",
                        "payment_date" : "2020-05-01T00:00:00"
                    },
                    {
                        "id"           : 1,
                        "order_number" : "8UVNSN0Z9IG4",
                        "product"      : "비누",
                        "payment_date" : "2019-03-01T00:24:00"
                    }
                ]
            }
        )
        self.assertEqual(response.status_code, 200)

class OrderListTest(TestCase):
    def setUp(self):
        Gender.objects.create(
            id     = 1,
            gender = "Woman"
        )

        User.objects.create(
            id           = 1,
            name         = "홍",
            nickname     = "dev",
            password     = "1234567aA!",
            phone_number = "01012345678",
            email        = "hong1@gamil.com",
            gender       = Gender.objects.get(id = 1)
        )

        User.objects.create(
            id           = 2,
            name         = "박",
            nickname     = "devdev",
            password     = "1234567bB@",
            phone_number = "01012345678",
            email        = "park2@gamil.com",
            gender       = Gender.objects.get(id = 1)
        )

        User.objects.create(
            id           = 3,
            name         = "김",
            nickname     = "devkim",
            password     = "1234567cC#",
            phone_number = "01012345678",
            email        = "kim@gamil.com",
            gender       = Gender.objects.get(id = 1)
        )

        Order.objects.create(
            id           = 1,
            user         = User.objects.get(id = 1),
            order_number = "8UVNSN0Z9IG4",
            product      = "옛날 비누",
            payment_date = "2019-03-01T00:24:00"
        )

        Order.objects.create(
            id           = 2,
            user         = User.objects.get(id = 1),
            order_number = "MDT30FXBKY5J",
            product      = "최근 비누",
            payment_date = "2020-05-01"
        )

        Order.objects.create(
            id           = 3,
            user         = User.objects.get(id = 2),
            order_number = "T4LV8J9BUE3U",
            product      = "최근 책갈피",
            payment_date = "2018-03-01T00:24:00"
        )

        Order.objects.create(
            id           = 4,
            user         = User.objects.get(id = 2),
            order_number = "QX2JQWYL5GVU",
            product      = "옛날 책갈피",
            payment_date = "2017-05-01"
        )

    def tearDown(self):
        Gender.objects.all().delete()
        User.objects.all().delete()
        Order.objects.all().delete()

    def test_order_list_get_success(self):
        response = Client().get('/order/list')

        self.assertEqual(response.json(),
            {
                "orders": [
                    {
                        "id": 2,
                        "user_id": 1,
                        "user_name": "홍",
                        "user_email": "hong1@gamil.com",
                        "order_number": "MDT30FXBKY5J",
                        "product": "최근 비누",
                        "payment_date": "2020-05-01T00:00:00"
                    },
                    {
                        "id": 3,
                        "user_id": 2,
                        "user_name": "박",
                        "user_email": "park2@gamil.com",
                        "order_number": "T4LV8J9BUE3U",
                        "product": "최근 책갈피",
                        "payment_date": "2018-03-01T00:24:00"
                    }
                ]
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_order_list_get_search_name_success(self):
        response = Client().get('/order/list?name=홍')

        self.assertEqual(response.json(),
            {
                "orders": [
                    {
                        "id": 2,
                        "user_id": 1,
                        "user_name": "홍",
                        "user_email": "hong1@gamil.com",
                        "order_number": "MDT30FXBKY5J",
                        "product": "최근 비누",
                        "payment_date": "2020-05-01T00:00:00"
                    }
                ]
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_order_list_get_search_email_success(self):
        response = Client().get('/order/list?email=hong1')

        self.assertEqual(response.json(),
            {
                "orders": [
                    {
                        "id": 2,
                        "user_id": 1,
                        "user_name": "홍",
                        "user_email": "hong1@gamil.com",
                        "order_number": "MDT30FXBKY5J",
                        "product": "최근 비누",
                        "payment_date": "2020-05-01T00:00:00"
                    }
                ]
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_order_list_get_search_name_fail(self):
        response = Client().get('/order/list?name=김')

        self.assertEqual(response.json(),
            {
                "error" : "ORDER_DOES_NOT_EXIST"
            }
        )
        self.assertEqual(response.status_code, 400)

    def test_order_list_get_search_email_fail(self):
        response = Client().get('/order/list?email=kim1')

        self.assertEqual(response.json(),
            {
                "error" : "ORDER_DOES_NOT_EXIST"
            }
        )
        self.assertEqual(response.status_code, 400)
