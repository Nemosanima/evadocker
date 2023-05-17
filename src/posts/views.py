from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from tools.functions.paginator import page

from .forms import CommentForm, GroupCreateForm, GroupEditForm, PostForm
from .models import Group, Post


@login_required
def search(request):
    search_query = request.GET.get('search', '')
    if search_query:
        posts = Post.objects.filter(Q(author__username__icontains=search_query) |
                                    Q(text__icontains=search_query) |
                                    Q(author__first_name__icontains=search_query) |
                                    Q(author__last_name__icontains=search_query) |
                                    Q(group__title__icontains=search_query) |
                                    Q(group__description__icontains=search_query)
                                    )
    else:
        posts = Post.objects.all()

    if posts.count() == 0:
        title = 'Соответствий не найдено'
    else:
        title = 'Все то, что удалось найти'
    context = {
        'title': title,
        'page_obj': page(posts, request)
    }
    return render(request, 'posts/search.html', context)


def index(request):
    posts = Post.objects.all()
    context = {
        'title': 'Последние обнавления',
        'page_obj': page(posts, request)
    }
    return render(request, 'posts/index.html', context)


def group(request, group_slug):
    group = get_object_or_404(Group, slug=group_slug)
    posts = group.posts.all()
    context = {
        'group': group,
        'page_obj': page(posts, request)
    }
    return render(request, 'posts/group.html', context)


def groups_list(request):
    groups = Group.objects.all()
    context = {
        'title': 'Список групп',
        'page_obj': page(groups, request)
    }
    return render(request, 'posts/groups_list.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm()
    comments = post.comments.all()
    context = {
        'post': post,
        'form': form,
        'comments': comments

    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    if request.method == 'GET':
        # пустая форму для GET, т.к мы только создаем пост
        form = PostForm()
        context = {
            'form': form,
            'is_edit': False
        }
        return render(request, 'posts/post_create.html', context)
    # в request.POST содержуться данные, а в request.FILES файлы, т.е
    # поле FileField, ImageField
    form = PostForm(request.POST, files=request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('users:profile_posts', username=post.author)
    return render(request, 'posts/post_create.html', {'form': form, 'is_edit': False})


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author:
        raise PermissionDenied()
    if request.method == 'GET':
        form = PostForm(instance=post)
        context = {
            'form': form,
            'is_edi': True
        }
        return render(request, 'posts/post_create.html', context)
    # instance=post обязательно, иначе нужно обьявлять автора и
    # посты будут создаваться новые, а не редактироваться
    form = PostForm(request.POST, files=request.FILES or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id=post.id)
    return render(request, 'posts/post_create.html', {'form': form, 'is_edit': True})


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def group_create(request):
    if request.method == 'GET':
        form = GroupCreateForm()
        return render(request, 'posts/group_create.html', {'form': form})
    form = GroupCreateForm(request.POST)
    if form.is_valid():
        group = form.save(commit=False)
        group.admin = request.user
        group.save()
        return redirect('posts:groups_list')
    return render(request, 'posts/group_create.html', {'form': form})


@login_required
def group_edit(request, group_slug):
    group = get_object_or_404(Group, slug=group_slug)
    if request.user != group.admin:
        raise PermissionDenied()
    if request.method == 'GET':
        form = GroupEditForm(instance=group)
        return render(request, 'posts/group_edit.html', {'form': form, 'group': group})
    form = GroupEditForm(request.POST, instance=group)
    if form.is_valid():
        form.save()
        return redirect('posts:groups_list')
    return render(request, 'posts/group_edit.html', {'form': form, 'group': group})


@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author:
        raise PermissionDenied()
    if request.method == 'POST':
        post.delete()
        return redirect('users:profile_posts', post.author.username)
    raise PermissionDenied()


@login_required
def group_delete(request, group_slug):
    group = get_object_or_404(Group, slug=group_slug)
    if request.user != group.admin:
        raise PermissionDenied()
    if request.method == 'POST':
        group.delete()
        return redirect('posts:groups_list')
    raise PermissionDenied()
