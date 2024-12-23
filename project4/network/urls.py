
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create, name="create"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("following", views.following, name="following"),
    path("<str:username>", views.user_page, name="user_page"),
    path("post/<int:post_id>", views.comment, name="comment" ),

    path("post/<int:post_id>/add", views.add_comment, name="api-add_comment"),
    path("network/<int:post_id>", views.edit, name="api_edit"),
    path("like/<int:post_id>", views.like, name="api-like"),
    path("follow/<str:user1>", views.follow, name="api-follow"),
]
