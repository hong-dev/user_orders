from .views import OrderView, OrderDetailView

from django.urls import path

urlpatterns = [
    path('', OrderView.as_view()),
    path('/detail', OrderDetailView.as_view())
]
