from .views import SignUpView, SignInView, UserInfoView, LogOutView

from django.urls import path

urlpatterns = [
    path('/sign-up', SignUpView.as_view()),
    path('/sign-in', SignInView.as_view()),
    path('/log-out', LogOutView.as_view()),
    path('/info', UserInfoView.as_view())
]
