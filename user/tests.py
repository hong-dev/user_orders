import json
import bcrypt
import jwt

from .models          import Gender, User
from project.settings import SECRET_KEY, ALGORITHM

from django.test import TestCase, Client

class SignUpTest(TestCase):
    def setUp(self):
        Gender.objects.create(
            id     = 1,
            gender = "Woman"
        )

        User.objects.create(
            id           = 1,
            name         = "홍홍",
            nickname     = "DevDev",
            password     = "1234",
            phone_number = "01012345678",
            email        = "honghong@gamil.com",
            gender       = Gender.objects.get(id = 1)
        )

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

        self.assertEqual(response.status_code, 201)

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

        self.assertEqual(response.status_code, 201)

    def test_sign_up_email_duplicate_fail(self):
        user_data = {
            "name"         : "홍",
            "nickname"     : "Dev",
            "password"     : "1234",
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
        self.assertEqual(response.status_code, 201)

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

class LogOutTest(TestCase):
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

    def test_logout_get_success(self):
        token = jwt.encode(
            {"email" : "hong@gamil.com"},
            SECRET_KEY,
            algorithm = ALGORITHM
        ).decode('utf-8')

        response = Client().get('/user/log-out',
                                **{'HTTP_Authorization' : token},
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
            name         = "홍1",
            nickname     = "Dev1",
            password     = bcrypt.hashpw("1234".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            phone_number = "01012345678",
            email        = "hong1@gamil.com",
            gender       = Gender.objects.get(id = 1)
        )

        User.objects.create(
            id           = 2,
            name         = "홍2",
            nickname     = "Dev2",
            password     = bcrypt.hashpw("1234".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            phone_number = "01012345678",
            email        = "hong2@gamil.com",
            gender       = None
        )

    def tearDown(self):
        Gender.objects.all().delete()
        User.objects.all().delete()

    def test_user_info_get_success(self):
        token = jwt.encode(
            {"email" : "hong1@gamil.com"},
            SECRET_KEY,
            algorithm = ALGORITHM
        ).decode('utf-8')

        response = Client().get('/user/info',
                                **{'HTTP_Authorization' : token},
                                content_type = 'application/json')

        self.assertEqual(response.json(),
            {
                "user_info" : {
                    "id"           : 1,
                    "name"         : "홍1",
                    "nickname"     : "Dev1",
                    "phone_number" : "01012345678",
                    "email"        : "hong1@gamil.com",
                    "gender"       : "Woman"
                }
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_user_info_get_gender_null_success(self):
        token = jwt.encode(
            {"email" : "hong2@gamil.com"},
            SECRET_KEY,
            algorithm = ALGORITHM
        ).decode('utf-8')

        response = Client().get('/user/info',
                                **{'HTTP_Authorization' : token},
                                content_type = 'application/json')

        self.assertEqual(response.json(),
            {
                "user_info" : {
                    "id"           : 2,
                    "name"         : "홍2",
                    "nickname"     : "Dev2",
                    "phone_number" : "01012345678",
                    "email"        : "hong2@gamil.com",
                    "gender"       : None
                }
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_user_info_get_token_fail(self):
        token = jwt.encode(
            {"email" : "hong@gamil.com"},
            "WRONG_SECRET_KEY",
            algorithm = ALGORITHM
        ).decode('utf-8')

        response = Client().get('/user/info',
                                **{'HTTP_Authorization' : token},
                                content_type = 'application/json')

        self.assertEqual(response.json(),
            {
                "error" : "INVALID_TOKEN"
            }
        )
        self.assertEqual(response.status_code, 400)

    def test_user_info_get_user_fail(self):
        token = jwt.encode(
            {"email" : "dev@gamil.com"},
            SECRET_KEY,
            algorithm = ALGORITHM
        ).decode('utf-8')

        response = Client().get('/user/info',
                                **{'HTTP_Authorization' : token},
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
