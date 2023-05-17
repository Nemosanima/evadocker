from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CommentViewSet, GroupViewSet, PostViewSet, follow_api,
                    followers_api, followings_api, unfollow_api)

app_name = 'api'

router_v1 = DefaultRouter()

router_v1.register('posts', PostViewSet, basename='posts')
router_v1.register('groups', GroupViewSet, basename='groups')
router_v1.register(
    r'posts/(?P<post_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
    path('v1/', include(router_v1.urls)),
    path('v1/follow/', follow_api, name='follow_view'),
    path('v1/unfollow/', unfollow_api, name='unfollow_api'),
    path('v1/followings/', followings_api, name='followings_api'),
    path('v1/followers/', followers_api, name='followers_api'),
]
