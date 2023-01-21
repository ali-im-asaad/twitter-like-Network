
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newPost", views.new_post, name="newPost"),
    path("following/<int:page_id>", views.tracking_list, name="following"),
    path("postCollective", views.post_collective, name="postCollective"),
    path("profile/<int:user_id>/page/<int:page_number>", views.show_profile, name="userPosts"),
]
