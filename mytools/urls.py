from django.urls import path

from . import views

urlpatterns = [
    # vulreport 页面
    path('disassembler/', views.disassembler, name='disassembler'),
    path('etherscan/', views.etherscansync, name='etherscan'),
    path('disassembler_ajax/', views.disassembler_ajax_handle, name='disassembler_ajax'),
    path('save_sol_ajax/', views.save_sol_ajax, name='save_sol_ajax'),
    path('update_list_ajax/', views.update_list_ajax, name='update_list_ajax'),
    path('get_sync_report/', views.get_sync_report, name='get_sync_report'),
    path('save_sync_each_file/', views.save_sync_each_file, name='save_sync_each_file'),
    path('del_sync_each_file/', views.del_sync_each_file, name='del_sync_each_file'),
    path('check_sync_each_file/', views.check_sync_each_file, name='check_sync_each_file'),

]
