from django.urls import path
from . import views

urlpatterns = [
    path("", views.user_login, name="login"),
    path("signup/", views.user_signup, name="signup"),
    path("company_signup/", views.company_signup, name="company signup"),
    path("company_login/", views.company_login, name="company signup")

]