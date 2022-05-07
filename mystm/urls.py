from django.urls import path

from . import views

urlpatterns = [
    # Home 页面
    path('', views.welcome, name='home'),
    path('index/', views.index, name='index'),
    # 文档页
    path('docs/', views.docs, name='docs'),
]
# handler400 = views.bad_request
# handler403 = views.permission_denied
# handler404 = views.page_not_found
# handler500 = views.server_error