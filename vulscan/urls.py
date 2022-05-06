from django.urls import path

from . import views

urlpatterns = [
    # Scan 页面
    path('vulscan/', views.vulscan, name='vulscan'),
    path('upload_handle/',views.upload_handle),
]
