from django.urls import path
from .views import Home,Login,Logout,Admin
urlpatterns = [
    path('',Home,name='Home'),
    path('Login/',Login,name='Login'),
    path('Logout/',Logout,name='Logout'),
    path('Admin/',Admin,name='Admin'),



]


