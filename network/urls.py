
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("following", views.followingPosts, name="following"),
    path("<str:usuario>", views.profile, name="profile"),

    # API Route 
    path("editPost/<str:post_id>", views.editPost, name="editPost")
]
