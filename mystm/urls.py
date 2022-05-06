from django.urls import path

from . import views

urlpatterns = [
    # Home 页面
    path('', views.welcome, name='home'),
    path('index/', views.index, name='index'),
    # 文档页
    path('docs/', views.docs, name='docs'),
]