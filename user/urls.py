from .views import SignUpView, SignInView, UserInfoView

from django.urls import path

urlpatterns = [
    path('/sign-up', SignUpView.as_view()),
    path('/sign-in', SignInView.as_view()),
    path('/info', UserInfoView.as_view())
]
