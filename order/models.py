from user.models import User

from django.db import models

class Order(models.Model):
    user         = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
    order_number = models.CharField(max_length = 12, unique = True)
    product      = models.CharField(max_length = 200)
    payment_date = models.DateTimeField()
    created_at   = models.DateTimeField(auto_now_add = True)
    updated_at   = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = 'orders'
