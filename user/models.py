from django.db import models

class Gender(models.Model):
    gender = models.CharField(max_length = 10)

    class Meta:
        db_table = 'genders'

class User(models.Model):
    gender       = models.ForeignKey('Gender', on_delete = models.SET_NULL, null = True)
    name         = models.CharField(max_length = 40)
    nickname     = models.CharField(max_length = 30)
    password     = models.CharField(max_length = 300)
    phone_number = models.CharField(max_length = 20)
    email        = models.EmailField(max_length = 100, unique = True)
    created_at   = models.DateTimeField(auto_now_add = True)
    updated_at   = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = 'users'
