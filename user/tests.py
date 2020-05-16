import json
import bcrypt

from .models import Gender, User

from django.test import TestCase, Client

class SignUpTest(TestCase):
    def setUp(self):
        Gender.objects.create(
            id     = 1,
            gender = "Woman"
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

class SignInTest(TestCase):
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

    def test_sign_in_post_success(self):
        user_data = {
            "email"    : "hong@gamil.com",
            "password" : "1234"
        }
        response = Client().post('/user/sign-in',
                                 json.dumps(user_data),
                                 content_type = 'application/json')

        self.assertEqual(response.json(),
            {
                "token" : "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6ImhvbmdAZ2FtaWwuY29tIn0.oWZ_v9icA4Ur_9Gs64ASOJ1rMaW_LCvU6tyG729f1m0"
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_sign_in_post_password_fail(self):
        user_data = {
            "email"    : "hong@gamil.com",
            "password" : "5678"
        }
        response = Client().post('/user/sign-in',
                                 json.dumps(user_data),
                                 content_type = 'application/json')

        self.assertEqual(response.json(),
            {
                "error" : "WRONG_PASSWORD"
            }
        )
        self.assertEqual(response.status_code, 401)

    def test_sign_in_post_email_fail(self):
        user_data = {
            "email"    : "dev@gamil.com",
            "password" : "1234"
        }
        response = Client().post('/user/sign-in',
                                 json.dumps(user_data),
                                 content_type = 'application/json')

        self.assertEqual(response.json(),
            {
                "error" : "USER_DOES_NOT_EXIST"
            }
        )
        self.assertEqual(response.status_code, 400)

    def test_sign_in_post_email_key_fail(self):
        user_data = {
            "password" : "5678"
        }
        response = Client().post('/user/sign-in',
                                 json.dumps(user_data),
                                 content_type = 'application/json')

        self.assertEqual(response.json(),
            {
                "error" : "INVALID_KEYS"
            }
        )
        self.assertEqual(response.status_code, 400)

    def test_sign_in_post_password_key_fail(self):
        user_data = {
            "email" : "hong@gamil.com"
        }
        response = Client().post('/user/sign-in',
                                 json.dumps(user_data),
                                 content_type = 'application/json')

        self.assertEqual(response.json(),
            {
                "error" : "INVALID_KEYS"
            }
        )
        self.assertEqual(response.status_code, 400)
