from django.urls import path
from . import views


app_name = 'users'
urlpatterns = [
    path('login', views.loginpage, name='loginpage'),
    path('logout', views.logoutuser, name='logout'),
    path('register', views.register, name='register'),
    path('user', views.userpage, name='userpage'),
]
