from django.urls import path
from . import views

urlpatterns = [
    path('groups/', views.group_list, name='group_list'),
    path('groups/<int:group_id>/', views.group_detail, name='group_detail'),
    path('groups/create/', views.create_group, name='create_group'),
    path('groups/<int:group_id>/update/', views.update_group, name='update_group'),
    path('groups/<int:group_id>/leave/', views.leave_group, name='leave_group'),
    path('groups/user/', views.user_group_list, name='user_group_list'),
    path('groups/<int:group_id>/chat/', views.group_chat, name='group_chat'),
]