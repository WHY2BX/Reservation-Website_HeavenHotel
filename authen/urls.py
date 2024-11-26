from django.urls import path

from authen.views import *


urlpatterns = [
    path('', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('register/', RegisterView.as_view(), name="register"),
    path('changepassword/', PasswordChangeView.as_view(), name="change_password")
]