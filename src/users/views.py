from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from posts.models import Post
from tools.functions.paginator import page

from .forms import CreationForm, ProfileDeleteForm, UserEditForm
from .models import Follow

User = get_user_model()


def signup_system(request):
    if request.method == 'GET':
        form = CreationForm()
        return render(request, 'users/signup.html', {'form': form})
    form = CreationForm(request.POST)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('posts:index')
    return render(request, 'users/signup.html', {'form': form})


@login_required()
def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = author.posts.all()[:3]
    number_of_posts = author.posts.all().count()
    following = Follow.objects.filter(
        user=request.user,
        author=author).exists()

    subscribers = author.followings.all()
    subscriptions = author.followers.all()

    context = {
        'author': author,
        'page_obj': posts,
        'number_of_posts': number_of_posts,
        'following': following,
        'subscriptions': subscriptions,
        'subscribers': subscribers
    }
    return render(request, 'users/profile.html', context)


@login_required
def profile_posts(request, username):
    author = get_object_or_404(User, username=username)
    posts = author.posts.all()
    context = {
        'author': author,
        'page_obj': page(posts, request)
    }
    return render(request, 'users/profile_posts.html', context)


@login_required
def profile_edit(request, username):
    user = get_object_or_404(User, username=username)
    if request.user != user:
        return redirect('users:profile', username=user.username)
    if request.method == 'GET':
        form = UserEditForm(instance=user)
        return render(request, 'users/profile_edit.html', {'form': form})
    form = UserEditForm(request.POST, instance=user)
    if form.is_valid():
        form.save()
        return redirect('users:profile', username)
    return render(request, 'users/profile_edit.html', {'form': form})


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    user = request.user
    if author != user:
        Follow.objects.get_or_create(user=user, author=author)
    return redirect('users:profile', username=username)


@login_required
def profile_unfollow(request, username):
    Follow.objects.get(user=request.user, author__username=username).delete()
    return redirect('users:profile', username=username)


@login_required
def follow(request):
    posts = Post.objects.filter(author__followings__user=request.user)
    if posts.count() == 0:
        title = 'Здесь будут ваши подписки'
    else:
        title = 'Избранные авторы'
    context = {
        'title': title,
        'page_obj': page(posts, request)
    }
    return render(request, 'users/follow.html', context)


@login_required
def profile_followers(request, username):
    author = get_object_or_404(User, username=username)
    followers = author.followings.all()
    if followers.count() == 0:
        title = 'Пока пусто'
    else:
        title = 'Подписчики'
    context = {
        'title': title,
        'page_obj': page(followers, request)
    }
    return render(request, 'users/profile_followers.html', context)


@login_required
def profile_followings(request, username):
    author = get_object_or_404(User, username=username)
    followings = author.followers.all()
    if followings.count() == 0:
        title = 'Пока пусто'
    else:
        title = 'Подписки'
    context = {
        'title': title,
        'page_obj': page(followings, request)
    }
    return render(request, 'users/profile_followings.html', context)


@login_required
def profile_delete(request, username):
    user = get_object_or_404(User, username=username)
    if request.user != user:
        return redirect('users:profile', username=request.user.username)
    if request.method == 'GET':
        form = ProfileDeleteForm()
        return render(request, 'users/profile_delete.html', {'form': form})
    form = ProfileDeleteForm(request.POST)
    password = request.POST['password']
    if user.check_password(password):
        user.delete()
        return redirect('posts:index')
    return render(request, 'users/profile_delete.html', {'form': form})
