from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from posts.models import Comment, Group, Post
from users.models import Follow

from .filters import PostFilter
from .permissions import IsAdminOfGroupOrReadOnly, IsAuthorOrReadOnly
from .serializers import (CommentSerializer, CustomUserSerializer,
                          FollowersSerializer, FollowingsSerializer,
                          FollowSerializer, GroupPostSerializer,
                          GroupSerializer, PostSerializer)

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    serializer_class = CustomUserSerializer
    queryset = User.objects.all()


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PostFilter
    permission_classes = (IsAuthorOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    lookup_field = 'slug'
    permission_classes = (IsAdminOfGroupOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return GroupPostSerializer
        return GroupSerializer

    def perform_create(self, serializer):
        serializer.save(admin=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        return post.comments.all()

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        serializer.save(author=self.request.user, post=post)


@api_view(['POST'])
def follow_api(request):
    username_of_author = request.data.get('author')
    author = get_object_or_404(User, username=username_of_author)
    user = request.user
    if Follow.objects.filter(author=author, user=user).exists():
        return Response(
            {'error':
             f'Вы уже подписаны на пользователя {username_of_author}'},
            status=status.HTTP_400_BAD_REQUEST
        )
    if author == user:
        return Response({'error': 'Нельзя подписываться на себя'},
                        status=status.HTTP_400_BAD_REQUEST)
    serializer = FollowSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def unfollow_api(request):
    username_of_author = request.data.get('author')
    author = get_object_or_404(User, username=username_of_author)
    user = request.user
    if Follow.objects.filter(author=author, user=user).exists():
        Follow.objects.filter(author=author, user=user).delete()
        return Response(status=status.HTTP_200_OK)
    return Response({'error': f'Вы не подписаны на {username_of_author}'},
                    status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def followings_api(request):
    user = request.user
    followings = user.followers.all()
    serializer = FollowingsSerializer(followings, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def followers_api(request):
    user = request.user
    followers = user.followings.all()
    serializer = FollowersSerializer(followers, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
