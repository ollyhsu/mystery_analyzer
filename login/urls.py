from . import views
from django.urls import path

urlpatterns = [
    path('login/', views.login, name='login'),
    path('login_out/', views.login_out, name="login_out"),
    path('register/', views.register, name="register"),
]