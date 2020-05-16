from .views import OrderView

from django.urls import path

urlpatterns = [
    path('', OrderView.as_view())
]
