from django.urls import path

from . import views

urlpatterns = [
    # vulreport 页面
    path('disassembler/', views.disassembler, name='disassembler'),
    path('etherscan/', views.etherscansync, name='etherscan'),
    path('disassembler_ajax/', views.disassembler_ajax_handle, name='disassembler_ajax'),
]
