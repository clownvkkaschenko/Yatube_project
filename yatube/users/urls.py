from django.urls import path
from . import views

from django.contrib.auth.views import (
    LogoutView, LoginView,
    PasswordChangeView, PasswordChangeDoneView,
    PasswordResetView, PasswordResetDoneView,
    PasswordResetCompleteView, PasswordResetConfirmView
)


app_name = 'users'

urlpatterns = [
    #  registration on the website
    path('signup/', views.SignUp.as_view(), name='signup'),
    #  window at the end of work in the account
    path(
        'logout/',
        LogoutView.as_view(
            template_name='users/logged_out.html'),
        name='logout'
    ),
    #  login to your account
    path(
        'login/',
        LoginView.as_view(
            template_name='users/login.html'),
        name='login'
    ),
    #  password reset via email
    path(
        'password_reset/',
        PasswordResetView.as_view(
            template_name='users/password_reset_form.html'),
        name='password_reset'
    ),
    #  email notification
    path(
        'password_reset/done/',
        PasswordResetDoneView.as_view(
            template_name='users/password_reset_done.html'),
        name='password_reset_done'
    ),
    #  password change form via email
    path(
        'reset/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(
            template_name='users/password_reset_confirm.html'),
        name='password_reset_confirm'
    ),
    #  password reset via email successful
    path(
        'reset/done/',
        PasswordResetCompleteView.as_view(
            template_name='users/password_reset_complete.html'),
        name='password_reset_complete'
    ),
    #  password change
    path(
        'password_change/',
        PasswordChangeView.as_view(
            template_name='users/password_change_form.html'),
        name='password_change'
    ),
    #  password reset successful
    path(
        'password_change/done/',
        PasswordChangeDoneView.as_view(
            template_name='users/password_change_done.html'),
        name='password_change_done'
    ),
]
