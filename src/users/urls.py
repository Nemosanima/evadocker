from django.contrib.auth.views import (LoginView, LogoutView,
                                       PasswordChangeDoneView,
                                       PasswordChangeView,
                                       PasswordResetCompleteView,
                                       PasswordResetConfirmView,
                                       PasswordResetDoneView,
                                       PasswordResetView)
from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('signup/',
         views.signup_system,
         name='signup'),
    path(
        'logout/',
        LogoutView.as_view(template_name='users/logged_out.html'),
        name='logout'
    ),
    path(
        'login/',
        LoginView.as_view(template_name='users/login.html'),
        name='login'),
    path('password_change/',
         PasswordChangeView.as_view(template_name='users/password_change_form.html'),
         name='password_change_form'),
    path('password_change/done/',
         PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'),
         name='password_change_done'),
    path('password_reset/',
         PasswordResetView.as_view(template_name='users/password_reset_form.html'),
         name='password_reset_form'),
    path('password_reset/done/',
         PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/done/',
         PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
    # for profile
    path('profile/<str:username>/', views.profile, name='profile'),
    # for posts of a certain user
    path('profile/<str:username>/posts/', views.profile_posts, name='profile_posts'),
    # for edit profile
    path('profile/<str:username>/edit/', views.profile_edit, name='profile_edit'),
    # for follow
    path('profile/<str:username>/follow/', views.profile_follow, name='profile_follow'),
    # for unfollow
    path('profile/<str:username>/unfollow/', views.profile_unfollow, name='profile_unfollow'),
    # favorites users
    path('follow/', views.follow, name='follow'),
    # for page with followers of a certain user
    path('profile/<str:username>/followers/', views.profile_followers, name='profile_followers'),
    # for page with followings of a certain user
    path('profile/<str:username>/followings/', views.profile_followings, name='profile_followings'),
    # for delete an account
    path('profile/<str:username>/delete/', views.profile_delete, name='profile_delete')
]
