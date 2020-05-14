DATABASES = {
    'default' : {
        'ENGINE'  : 'django.db.backends.mysql',
        'NAME'    : 'project',
        'USER'    : 'root',     #DB접속 계정명
        'PASSWORD': 'password', #DB접속용 비밀번호
        'HOST'    : 'localhost',
        'PORT'    : '3306',
        'OPTIONS' : {
            'init_command': 'SET default_storage_engine=INNODB'
        }
    }
}

SECRET = {
    'secret'    : '*&pe!w1_!h4ndsuc58g4wawqv4$$dybb8-8+$v$z1f+nap+ar-',
    'algorithm' : 'HS256'
}


