from django.urls import path

from . import views

app_name = 'posts'

urlpatterns = [
    # for home page
    path('', views.index, name='index'),
    # for posts of a certain group
    path('group/<slug:group_slug>/', views.group, name='group'),
    # for a list of groups
    path('groups_list/', views.groups_list, name='groups_list'),
    # for a certain post
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    # for creating a post
    path('post_create/', views.post_create, name='post_create'),
    # for editing a post
    path('posts/<int:post_id>/edit/', views.post_edit, name='post_edit'),
    # for processing comments
    path('posts/<int:post_id>/comment/',
         views.add_comment,
         name='add_comment'),
    # for creating a group
    path('group_create/', views.group_create, name='group_create'),
    # for editing a group
    path('groups/<slug:group_slug>/edit/',
         views.group_edit,
         name='group_edit'),
    # to delete a post
    path('posts/<int:post_id>/delete/',
         views.post_delete,
         name='post_delete'),
    # to delete a group
    path('groups/<slug:group_slug>/delete/',
         views.group_delete,
         name='group_delete'),
    # for search
    path('search/', views.search, name='search')
]
