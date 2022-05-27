from django.contrib.auth.views import (LogoutView, LoginView,
                                      PasswordChangeView, PasswordChangeDoneView,
                                      PasswordResetView)
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    #  зарегестрироваться
    path('signup/', views.SignUp.as_view(), name='signup'),
    #  окно при выходе из аккаунта
    path(
      'logout/',
      LogoutView.as_view(template_name='users/logged_out.html'),
      name='logout'
    ),
    #  войти
    path(
      'login/',
      LoginView.as_view(template_name='users/login.html'),
      name='login'
    ),
    #  сброс пароля через почту
    path(
      'password_reset_form/',
      PasswordResetView.as_view(template_name='users/password_reset_form.html'),
      name = 'password_reset_form'
    ),
    #  смена пароля
    path(
      'password_change/',
      PasswordChangeView.as_view(template_name='users/password_change_form.html'),
      name = 'password_change'
    ),
    #  окно при успешной смене пароля
    path(
      'password_change/done/',
      PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'),
      name = 'password_change_done'
    ),
]
