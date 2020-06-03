import json
import bcrypt
import jwt
import string
import random

from .models          import Gender, User
from project.settings import SECRET_KEY, ALGORITHM

from django.test       import TestCase, Client
from django.core.cache import cache

class SignUpTest(TestCase):
    def setUp(self):
        Gender.objects.create(
            id     = 1,
            gender = "Woman"
        )

        User.objects.create(
            id           = 1,
            name         = "홍홍",
            nickname     = "devdev",
            password     = "12345678aA!",
            phone_number = "01012345678",
            email        = "honghong@gamil.com",
            gender       = Gender.objects.get(id = 1)
        )

    def test_sign_up_post_success(self):
        user_data = {
            "name"         : "홍",
            "nickname"     : "dev",
            "password"     : "1234567aA!",
            "phone_number" : "01012345678",
            "email"        : "hong@gamil.com",
            "gender"       : "Woman"
        }
        response = Client().post('/user/sign-up',
                                 json.dumps(user_data),
                                 content_type = 'application/json')

        self.assertEqual(response.status_code, 201)

    def test_sign_up_post_without_gender_success(self):
        user_data = {
            "name"         : "홍",
            "nickname"     : "dev",
            "password"     : "1234567aA!",
            "phone_number" : "01012345678",
            "email"        : "hong@gamil.com",
        }
        response = Client().post('/user/sign-up',
                                 json.dumps(user_data),
                                 content_type = 'application/json')

        self.assertEqual(response.status_code, 201)

    def test_sign_up_email_duplicate_fail(self):
        user_data = {
            "name"         : "홍",
            "nickname"     : "dev",
            "password"     : "1234567aA!",
            "phone_number" : "01012345678",
            "email"        : "honghong@gamil.com",
            "gender"       : "Woman"
        }
        response = Client().post('/user/sign-up',
                                 json.dumps(user_data),
                                 content_type = 'application/json')

        self.assertEqual(response.json(),
            {
                "error" : "EMAIL_ALREADY_EXISTS"
            }
        )
        self.assertEqual(response.status_code, 409)

    def test_sign_up_name_key_fail(self):
        user_data = {
            "nickname"     : "dev",
            "password"     : "1234567aA!",
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
            "password"     : "1234567aA!",
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
            "nickname"     : "dev",
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
            "nickname"     : "dev",
            "password"     : "1234567aA!",
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
            "nickname"     : "dev",
            "password"     : "1234567aA!",
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
            "nickname"     : "dev",
            "password"     : "1234567aA!",
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

    def test_sign_up_post_email_type_at_fail(self):
        user_data = {
            "name"         : "홍",
            "nickname"     : "dev",
            "password"     : "1234567aA!",
            "phone_number" : "01012345678",
            "email"        : "honggamil.com",
            "gender"       : "Woman"
        }
        response = Client().post('/user/sign-up',
                                 json.dumps(user_data),
                                 content_type = 'application/json')

        self.assertEqual(response.json(),
            {
                "error" : "INVALID_TYPE"
            }
        )
        self.assertEqual(response.status_code, 400)

    def test_sign_up_post_email_type_dot_fail(self):
        user_data = {
            "name"         : "홍",
            "nickname"     : "dev",
            "password"     : "1234567aA!",
            "phone_number" : "01012345678",
            "email"        : "hong@gamilcom",
            "gender"       : "Woman"
        }
        response = Client().post('/user/sign-up',
                                 json.dumps(user_data),
                                 content_type = 'application/json')

        self.assertEqual(response.json(),
            {
                "error" : "INVALID_TYPE"
            }
        )
        self.assertEqual(response.status_code, 400)

    def test_sign_up_post_phone_type_fail(self):
        user_data = {
            "name"         : "홍",
            "nickname"     : "dev",
            "password"     : "1234567aA!",
            "phone_number" : "dd01012345678",
            "email"        : "hong@gamil.com",
            "gender"       : "Woman"
        }
        response = Client().post('/user/sign-up',
                                 json.dumps(user_data),
                                 content_type = 'application/json')

        self.assertEqual(response.json(),
            {
                "error" : "INVALID_TYPE"
            }
        )
        self.assertEqual(response.status_code, 400)

    def test_sign_up_post_nick_kor_fail(self):
        user_data = {
            "name"         : "홍",
            "nickname"     : "홍",
            "password"     : "1234567aA!",
            "phone_number" : "01012345678",
            "email"        : "hong@gamil.com",
            "gender"       : "Woman"
        }
        response = Client().post('/user/sign-up',
                                 json.dumps(user_data),
                                 content_type = 'application/json')

        self.assertEqual(response.json(),
            {
                "error" : "INVALID_NICKNAME"
            }
        )
        self.assertEqual(response.status_code, 400)

    def test_sign_up_post_nick_capital_fail(self):
        user_data = {
            "name"         : "홍",
            "nickname"     : "DEV",
            "password"     : "1234567aA!",
            "phone_number" : "01012345678",
            "email"        : "hong@gamil.com",
            "gender"       : "Woman"
        }
        response = Client().post('/user/sign-up',
                                 json.dumps(user_data),
                                 content_type = 'application/json')

        self.assertEqual(response.json(),
            {
                "error" : "INVALID_NICKNAME"
            }
        )
        self.assertEqual(response.status_code, 400)

    def test_sign_up_post_nick_num_fail(self):
        user_data = {
            "name"         : "홍",
            "nickname"     : "123",
            "password"     : "1234567aA!",
            "phone_number" : "01012345678",
            "email"        : "hong@gamil.com",
            "gender"       : "Woman"
        }
        response = Client().post('/user/sign-up',
                                 json.dumps(user_data),
                                 content_type = 'application/json')

        self.assertEqual(response.json(),
            {
                "error" : "INVALID_NICKNAME"
            }
        )
        self.assertEqual(response.status_code, 400)

    def test_sign_up_post_nick_special_fail(self):
        user_data = {
            "name"         : "홍",
            "nickname"     : "dev!!",
            "password"     : "1234567aA!",
            "phone_number" : "01012345678",
            "email"        : "hong@gamil.com",
            "gender"       : "Woman"
        }
        response = Client().post('/user/sign-up',
                                 json.dumps(user_data),
                                 content_type = 'application/json')

        self.assertEqual(response.json(),
            {
                "error" : "INVALID_NICKNAME"
            }
        )
        self.assertEqual(response.status_code, 400)

    def test_sign_up_post_pw_capital_fail(self):
        user_data = {
            "name"         : "홍",
            "nickname"     : "dev",
            "password"     : "12345678a@",
            "phone_number" : "01012345678",
            "email"        : "hong@gamil.com",
            "gender"       : "Woman"
        }
        response = Client().post('/user/sign-up',
                                 json.dumps(user_data),
                                 content_type = 'application/json')

        self.assertEqual(response.json(),
            {
                "error" : "INVALID_PASSWORD"
            }
        )
        self.assertEqual(response.status_code, 400)

    def test_sign_up_post_pw_lower_fail(self):
        user_data = {
            "name"         : "홍",
            "nickname"     : "dev",
            "password"     : "12345678A@",
            "phone_number" : "01012345678",
            "email"        : "hong@gamil.com",
            "gender"       : "Woman"
        }
        response = Client().post('/user/sign-up',
                                 json.dumps(user_data),
                                 content_type = 'application/json')

        self.assertEqual(response.json(),
            {
                "error" : "INVALID_PASSWORD"
            }
        )
        self.assertEqual(response.status_code, 400)

    def test_sign_up_post_pw_special_fail(self):
        user_data = {
            "name"         : "홍",
            "nickname"     : "dev",
            "password"     : "12345678aA",
            "phone_number" : "01012345678",
            "email"        : "hong@gamil.com",
            "gender"       : "Woman"
        }
        response = Client().post('/user/sign-up',
                                 json.dumps(user_data),
                                 content_type = 'application/json')

        self.assertEqual(response.json(),
            {
                "error" : "INVALID_PASSWORD"
            }
        )
        self.assertEqual(response.status_code, 400)

    def test_sign_up_post_pw_num_fail(self):
        user_data = {
            "name"         : "홍",
            "nickname"     : "dev",
            "password"     : "aaaaAAA!@#",
            "phone_number" : "01012345678",
            "email"        : "hong@gamil.com",
            "gender"       : "Woman"
        }
        response = Client().post('/user/sign-up',
                                 json.dumps(user_data),
                                 content_type = 'application/json')

        self.assertEqual(response.json(),
            {
                "error" : "INVALID_PASSWORD"
            }
        )
        self.assertEqual(response.status_code, 400)

    def test_sign_up_post_pw_length_fail(self):
        user_data = {
            "name"         : "홍",
            "nickname"     : "dev",
            "password"     : "123aA@",
            "phone_number" : "01012345678",
            "email"        : "hong@gamil.com",
            "gender"       : "Woman"
        }
        response = Client().post('/user/sign-up',
                                 json.dumps(user_data),
                                 content_type = 'application/json')

        self.assertEqual(response.json(),
            {
                "error" : "INVALID_PASSWORD"
            }
        )
        self.assertEqual(response.status_code, 400)

    def test_sign_up_post_name_num_fail(self):
        user_data = {
            "name"         : "홍1",
            "nickname"     : "dev",
            "password"     : "1234567aA@",
            "phone_number" : "01012345678",
            "email"        : "hong@gamil.com",
            "gender"       : "Woman"
        }
        response = Client().post('/user/sign-up',
                                 json.dumps(user_data),
                                 content_type = 'application/json')

        self.assertEqual(response.json(),
            {
                "error" : "INVALID_NAME"
            }
        )
        self.assertEqual(response.status_code, 400)

    def test_sign_up_post_name_special_fail(self):
        user_data = {
            "name"         : "홍!!",
            "nickname"     : "dev",
            "password"     : "1234567aA@",
            "phone_number" : "01012345678",
            "email"        : "hong@gamil.com",
            "gender"       : "Woman"
        }
        response = Client().post('/user/sign-up',
                                 json.dumps(user_data),
                                 content_type = 'application/json')

        self.assertEqual(response.json(),
            {
                "error" : "INVALID_NAME"
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

    def test_sign_in_post_success(self):
        user_data = {
            "email"    : "hong@gamil.com",
            "password" : "1234567aA!"
        }
        response = Client().post('/user/sign-in',
                                 json.dumps(user_data),
                                 content_type = 'application/json')

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
            "password" : "1234567aA!"
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
            "password" : "1234567aA!"
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

class LogOutTest(TestCase):
    def setUp(self):
        Gender.objects.create(
            id     = 1,
            gender = "Woman"
        )

        User.objects.create(
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

    def test_logout_get_success(self):
        user_number = ''.join(random.choice(string.ascii_uppercase + string.digits)
                   for x in range(12))

        token = jwt.encode(
            {"email" : "hong@gamil.com"},
            SECRET_KEY,
            algorithm = ALGORITHM
        ).decode('utf-8')

        cache.get_or_set(user_number, token)

        response = Client().get('/user/log-out',
                                **{'HTTP_Authorization' : user_number},
                                content_type = 'application/json')

        self.assertEqual(response.status_code, 200)

class UserInfoTest(TestCase):
    def setUp(self):
        Gender.objects.create(
            id     = 1,
            gender = "Woman"
        )

        User.objects.create(
            id           = 1,
            name         = "홍홍",
            nickname     = "devdev",
            password     = bcrypt.hashpw(
                "1234567aA!".encode('utf-8'),
                bcrypt.gensalt()
            ).decode('utf-8'),
            phone_number = "01012345678",
            email        = "hong1@gamil.com",
            gender       = Gender.objects.get(id = 1)
        )

        User.objects.create(
            id           = 2,
            name         = "홍",
            nickname     = "dev",
            password     = bcrypt.hashpw(
                "1234567bB@".encode('utf-8'),
                bcrypt.gensalt()
            ).decode('utf-8'),
            phone_number = "01012345678",
            email        = "hong2@gamil.com",
            gender       = None
        )

    def tearDown(self):
        Gender.objects.all().delete()
        User.objects.all().delete()

    def test_user_info_get_success(self):
        user_number = ''.join(random.choice(string.ascii_uppercase + string.digits)
                   for x in range(12))

        token = jwt.encode(
            {"email" : "hong1@gamil.com"},
            SECRET_KEY,
            algorithm = ALGORITHM
        ).decode('utf-8')

        cache.get_or_set(user_number, token)

        response = Client().get('/user/info',
                                **{'HTTP_Authorization' : user_number},
                                content_type = 'application/json')

        self.assertEqual(response.json(),
            {
                "user_info" : {
                    "id"           : 1,
                    "name"         : "홍홍",
                    "nickname"     : "devdev",
                    "phone_number" : "01012345678",
                    "email"        : "hong1@gamil.com",
                    "gender"       : "Woman"
                }
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_user_info_get_gender_null_success(self):
        user_number = ''.join(random.choice(string.ascii_uppercase + string.digits)
                   for x in range(12))

        token = jwt.encode(
            {"email" : "hong2@gamil.com"},
            SECRET_KEY,
            algorithm = ALGORITHM
        ).decode('utf-8')

        cache.get_or_set(user_number, token)

        response = Client().get('/user/info',
                                **{'HTTP_Authorization' : user_number},
                                content_type = 'application/json')

        self.assertEqual(response.json(),
            {
                "user_info" : {
                    "id"           : 2,
                    "name"         : "홍",
                    "nickname"     : "dev",
                    "phone_number" : "01012345678",
                    "email"        : "hong2@gamil.com",
                    "gender"       : None
                }
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_user_info_get_token_fail(self):
        user_number = ''.join(random.choice(string.ascii_uppercase + string.digits)
                   for x in range(12))

        token = jwt.encode(
            {"email" : "hong2@gamil.com"},
            SECRET_KEY,
            algorithm = ALGORITHM
        ).decode('utf-8')

        cache.get_or_set(user_number, token)

        response = Client().get('/user/info',
                                **{'HTTP_Authorization' : 'P1TUCSSWBLZR'},
                                content_type = 'application/json')

        self.assertEqual(response.json(),
            {
                "error" : "INVALID_TOKEN"
            }
        )
        self.assertEqual(response.status_code, 400)

    def test_user_info_get_user_fail(self):
        user_number = ''.join(random.choice(string.ascii_uppercase + string.digits)
                   for x in range(12))

        token = jwt.encode(
            {"email" : "hong@gamil.com"},
            SECRET_KEY,
            algorithm = ALGORITHM
        ).decode('utf-8')

        cache.get_or_set(user_number, token)

        response = Client().get('/user/info',
                                **{'HTTP_Authorization' : user_number},
                                content_type = 'application/json')

        self.assertEqual(response.json(),
            {
                "error" : "INVALID_USER"
            }
        )
        self.assertEqual(response.status_code, 401)

    def test_user_info_get_login_fail(self):
        response = Client().get('/user/info',
                                content_type = 'application/json')

        self.assertEqual(response.json(),
            {
                "error" : "LOGIN_REQUIRED"
            }
        )
        self.assertEqual(response.status_code, 401)
