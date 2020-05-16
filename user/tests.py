import json

from .models import Gender, User

from django.test import TestCase, Client

class SignUpTest(TestCase):
    def setUp(self):
        Gender.objects.create(
            id     = 1,
            gender = 'Woman'
        )

    def tearDown(self):
        Gender.objects.all().delete()

    def test_sign_up_post_success(self):
        user_data = {
            "name"         : "홍",
            "nickname"     : "Dev",
            "password"     : "1234",
            "phone_number" : "01012345678",
            "email"        : "hong@gamil.com",
            "gender"       : "Woman"
        }
        response = Client().post('/user/sign-up',
                                 json.dumps(user_data),
                                 content_type = 'application/json')

        self.assertEqual(response.status_code, 200)

    def test_sign_up_post_without_gender_success(self):
        user_data = {
            "name"         : "홍",
            "nickname"     : "Dev",
            "password"     : "1234",
            "phone_number" : "01012345678",
            "email"        : "hong@gamil.com",
        }
        response = Client().post('/user/sign-up',
                                 json.dumps(user_data),
                                 content_type = 'application/json')

        self.assertEqual(response.status_code, 200)

    def test_sign_up_name_key_fail(self):
        user_data = {
            "nickname"     : "Dev",
            "password"     : "1234",
            "phone_number" : "01012345678",
            "email"        : "hong@gamil.com",
            "gender"       : "Woman"
        }
        response = Client().post('/user/sign-up',
                                 json.dumps(user_data),
                                 content_type = 'application/json')

        self.assertEqual(response.json(),
            {
                "error" : "INVALID_KEYS"
            }
        )
        self.assertEqual(response.status_code, 400)

    def test_sign_up_nick_key_fail(self):
        user_data = {
            "name"         : "홍",
            "password"     : "1234",
            "phone_number" : "01012345678",
            "email"        : "hong@gamil.com",
            "gender"       : "Woman"
        }
        response = Client().post('/user/sign-up',
                                 json.dumps(user_data),
                                 content_type = 'application/json')

        self.assertEqual(response.json(),
            {
                "error" : "INVALID_KEYS"
            }
        )
        self.assertEqual(response.status_code, 400)

    def test_sign_up_password_key_fail(self):
        user_data = {
            "name"         : "홍",
            "nickname"     : "Dev",
            "phone_number" : "01012345678",
            "email"        : "hong@gamil.com",
            "gender"       : "Woman"
        }
        response = Client().post('/user/sign-up',
                                 json.dumps(user_data),
                                 content_type = 'application/json')

        self.assertEqual(response.json(),
            {
                "error" : "INVALID_KEYS"
            }
        )
        self.assertEqual(response.status_code, 400)

    def test_sign_up_phone_key_fail(self):
        user_data = {
            "name"         : "홍",
            "nickname"     : "Dev",
            "password"     : "1234",
            "email"        : "hong@gamil.com",
            "gender"       : "Woman"
        }
        response = Client().post('/user/sign-up',
                                 json.dumps(user_data),
                                 content_type = 'application/json')

        self.assertEqual(response.json(),
            {
                "error" : "INVALID_KEYS"
            }
        )
        self.assertEqual(response.status_code, 400)

    def test_sign_up_email_key_fail(self):
        user_data = {
            "name"         : "홍",
            "nickname"     : "Dev",
            "password"     : "1234",
            "phone_number" : "01012345678",
            "gender"       : "Woman"
        }
        response = Client().post('/user/sign-up',
                                 json.dumps(user_data),
                                 content_type = 'application/json')

        self.assertEqual(response.json(),
            {
                "error" : "INVALID_KEYS"
            }
        )
        self.assertEqual(response.status_code, 400)

    def test_sign_up_gender_fail(self):
        user_data = {
            "name"         : "홍",
            "nickname"     : "Dev",
            "password"     : "1234",
            "phone_number" : "01012345678",
            "email"        : "hong@gamil.com",
            "gender"       : "W"
        }
        response = Client().post('/user/sign-up',
                                 json.dumps(user_data),
                                 content_type = 'application/json')

        self.assertEqual(response.json(),
            {
                "error" : "GENDER_DOES_NOT_EXIST"
            }
        )
        self.assertEqual(response.status_code, 400)
