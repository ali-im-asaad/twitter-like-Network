import json
from django import http
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.utils import ProgrammingError
from django.http import HttpResponse, HttpResponseRedirect, request
from django.http.response import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .models import User, Posts, Like , Follower

def index(request):
    if request.method == "POST":
        is_authenticated = request.user.is_authenticated
        content = request.POST["content"]
        Post.objects.create(content=content, user=request.user) if is_authenticated else HttpResponseRedirect(reverse("index"))

    else:
        all_users_posts = Posts.objects.all().order_by("-time")
        paginator = Paginator(all_users_posts, 10)
        page_number = request.GET.get('page')
        page_paginator = paginator.get_page(page_number)
        return render(request, "network/index.html", {
            "page_paginator": page_paginator
        })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            user_f = Follower(user_follower=user)
            user_f.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def new_post(request):
    if request.method == "POST":
        post = Posts(user=request.user, content=request.POST["content"])
        post.save()
        return HttpResponseRedirect(reverse('index'))

    return HttpResponse("Error: This page only accepts post requests")



def tracking_list(request, page_id):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        followed_users = user.followers.values_list("user_follower", flat=True)
        posts = Posts.objects.filter(user__in=followed_users).order_by("-time")
        paginator = Paginator(posts, 10)
        page_number = request.GET.get("page")
        page_paginator = paginator.get_page(page_number)
        context = {
            "page_paginator": page_paginator,
            "followed_users": followed_users,
            "posts": posts,
            "pages": "following",
        }
        return render(request, "network/index.html", context)
    else:
        return redirect("login")


@csrf_exempt
def post_collective(request):
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."}, status=400)

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    data = json.loads(request.body)
    post = Posts.objects.get(id=data.get("postId", ""))

    post.content = data.get("content", post.content)

    if not data.get("switchLike", False) or request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    post.save()
    return JsonResponse({"message": "Successful editing of the post!", "number_of_likes": post.likes.count()}, status=201)


@csrf_exempt
def show_profile(request, user_id, page_number):
               
        if request.method == "POST":

            user_followed = User.objects.get(pk=user_id)
            user_following = request.user
            follow_data = user_followed.follows.first()

            istt_following = user_following in follow_data.followers.all()
            follow_data.followers.remove(user_following) if istt_following else follow_data.followers.add(user_following)
            user_following.follows.first().followed.remove(user_followed) if istt_following else user_following.follows.first().followed.add(user_followed)

            return JsonResponse({
                "following_status": "Follow" if istt_following else "Unfollow",
                "followers": follow_data.followers.all().count(),
                "following": follow_data.followed.all().count()}, status=200)
          
        user_pr = User.objects.get(pk=user_id)
        user_posts = user_pr.user_posts.order_by("-time").all()
        paginator = Paginator(user_posts, 10)
        page_number = request.GET.get('page')
        page_paginator = paginator.get_page(page_number)
        followers = user_pr.follows.first().followers.all()
        

        ist_following = request.user in followers
        f_status = "Follow" if not ist_following else "Unfollow"
        followings = user_pr.follows.first().followed.all()

        return render(request, "network/profile.html", {
            "user_posts": user_pr.user_posts.order_by("-time").all(),
            "usrr": user_pr,
            "page_paginator": page_paginator,
            "followers": len(followers),
            "followings": len(followings),
            "buttonContent": f_status,
    })




