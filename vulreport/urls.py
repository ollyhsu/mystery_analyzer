from django.urls import path

from . import views

urlpatterns = [
    # vulreport 页面
    path('vulreport/', views.vulreport, name='vulreport'),
    path('get_report/', views.get_report, name='get_report'),
    # path('vuldetail/', views.vuldetail, name='vuldetail'),

]
