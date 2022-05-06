from django.urls import path

from . import views

urlpatterns = [
    # vulreport 页面
    path('vulreport/', views.vulreport, name='vulreport'),
]
