from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('login', views.loginpage, name='loginpage'),
    path('logout', views.logoutuser, name='logout'),
    path('registrar', views.register, name='register'),
    path('usuario', views.userpage, name='userpage'),
    path('perfil', views.profile, name='profile'),

    path('reset_password',
         auth_views.PasswordResetView.as_view(
             template_name='users/password_reset.html'),
         name='reset_password'),

    path('reset_password_sent',
         auth_views.PasswordResetDoneView.as_view(
             template_name='users/password_reset_sent.html'),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='users/password_reset_form.html'),
         name='password_reset_confirm'),

    path('reset_password_success',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='users/password_reset_done.html'),
         name='password_reset_complete'),

]
