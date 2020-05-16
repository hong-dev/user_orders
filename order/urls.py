from .views import OrderView, OrderDetailView, OrderListView

from django.urls import path

urlpatterns = [
    path('', OrderView.as_view()),
    path('/detail', OrderDetailView.as_view()),
    path('/list', OrderListView.as_view())
]
