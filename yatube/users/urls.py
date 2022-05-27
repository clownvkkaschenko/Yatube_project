from django.contrib.auth.views import (LogoutView, LoginView,
                                      PasswordChangeView, PasswordChangeDoneView,
                                      PasswordResetView, PasswordResetDoneView,
                                      PasswordResetCompleteView, PasswordResetConfirmView)
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
      'password_reset/',
      PasswordResetView.as_view(template_name='users/password_reset_form.html'),
      name = 'password_reset'
    ),
    #  уведомление об отправкие ссылки на почту
    path(
      'password_reset/done/',
      PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
      name = 'password_reset_done'
    ),
    #  окошко со сбросом пороля через почту
    path(
      'reset/<uidb64>/<token>/',
      PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
      name='password_reset_confirm'
    ),
    #  сброс пароля прошёл успешно
    path('reset/done/',
    PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
    name = 'password_reset_complete'
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
