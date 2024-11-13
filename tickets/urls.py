from django.contrib.auth.views import LogoutView
from django.urls import path
from tickets import views

urlpatterns = [
    path('register/',views.register,name='register'),
    path('',views.login,name='login'),
    path('home/',views.home,name='home'),
    path('ticket/',views.ticket,name='ticket'),
    # path('ticket/<int:pk>',views.ticket,name='ticket_details'),
    path('ticket_list/',views.ticket_list,name='ticket_list'),
    path('logout/',views.logout,name='logout'),
    path('admin/tickets/', views.admin_ticket_list, name='admin_ticket_list'),
    path('admin/tickets/<int:ticket_id>/update/', views.update_ticket_status, name='update_ticket_status'),
    path('update/<int:pk>',views.update,name='update'),
    path('delete/<int:pk>',views.delete,name='delete'),
    path('ticket/<int:pk>/comments/', views.ticket_comments, name='ticket_comments')

]
