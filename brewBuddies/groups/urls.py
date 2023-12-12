from django.urls import path
from . import views

"""
URL patterns for the 'groups' app.

These patterns define the routes for various views related to group management within the application. Each path is associated with a specific view function and has a unique name to facilitate URL reversing.

URL Patterns:
- ''                     : Display a list of all groups.
- '<int:group_id>/'      : Display details for a specific group.
- 'create/'              : Create a new group.
- '<int:group_id>/update/': Update details of a specific group.
- '<int:group_id>/join/'  : Join a specific group.
- '<int:group_id>/leave/' : Leave a specific group.
- 'user/'                : Display a list of groups joined by the user.
- '<int:group_id>/chat/'  : Access the group chat for a specific group.
- 'map/'                 : Display a map with the locations of all groups.
- '<int:group_id>/delete/': Delete a specific group.

Note: '<int:group_id>/' represents a dynamic path parameter for the group's unique identifier.
"""

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