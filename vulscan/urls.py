from django.urls import path

from . import views

urlpatterns = [
    # Scan 页面
    path('vulscan/', views.vulscan, name='vulscan'),
    path('sol_upload_handle/', views.sol_upload_handle, name='sol_upload_handle'),
]
