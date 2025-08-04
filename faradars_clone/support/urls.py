from django.urls import path
from . import views

urlpatterns = [
    path('tickets/', views.ticket_list, name='ticket_list'),
    path('tickets/new/', views.ticket_create, name='ticket_create'),
    path('tickets/<int:pk>/', views.ticket_detail, name='ticket_detail'),
    path('tickets/<int:pk>/send/', views.ticket_send_message, name='ticket_send_message'),
    path('tickets/<int:pk>/messages/', views.ticket_messages_api, name='ticket_messages_api'),
]

from django.contrib.admin.views.decorators import staff_member_required

urlpatterns += [
    path('admin/tickets/', staff_member_required(views.admin_ticket_list), name='admin_ticket_list'),
    path('admin/tickets/<int:pk>/', staff_member_required(views.admin_ticket_detail), name='admin_ticket_detail'),
    path('admin/tickets/<int:pk>/close/', staff_member_required(views.close_ticket), name='close_ticket'),
]


urlpatterns += [
    path('admin/tickets/<int:pk>/send/', staff_member_required(views.admin_ticket_send_message), name='admin_ticket_send_message'),
]
