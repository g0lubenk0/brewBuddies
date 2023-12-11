from django.urls import path
from . import views

urlpatterns = [
    path('', views.group_list, name='group_list'),
    path('<int:group_id>/', views.group_detail, name='group_detail'),
    path('create/', views.create_group, name='create_group'),
    path('<int:group_id>/update/', views.update_group, name='update_group'),
    path('<int:group_id>/join/', views.join_group, name='join_group'),
    path('<int:group_id>/leave/', views.leave_group, name='leave_group'),
    path('user/', views.user_group_list, name='user_group_list'),
    path('<int:group_id>/chat/', views.group_chat, name='group_chat'),
    path('map/', views.map, name='map'),
    path('<int:group_id>/delete/', views.delete_group, name='delete_group'),
]