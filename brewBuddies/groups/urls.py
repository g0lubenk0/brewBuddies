from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_group, name='create'),
    path('details/<int:group_id>/', views.details_group, name='details'),
    path('join/<int:group_id>/', views.join_group, name='join'),
    path('leave/<int:group_id>/', views.leave_group, name='leave'),
    path('group_list/', views.groups, name='group_list'),
    path('user_groups/', views.user_groups_list, name='user_groups_list')
]
