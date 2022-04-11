from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import render
from django.urls import reverse
import json
from .models import User, Post
from django.core.paginator import Paginator

def likebutton(request, user, content):
    if request.method == "PUT":
        data = json.loads(content)
        userLiking = User.objects.get(username=user)
        postLiking = Post.objects.get(id=data["id"])

    if request.method == "PUT" and str(userLiking) in [i.username for i in postLiking.likes.all()] : 
        
        postLiking.likes.remove(userLiking)
        postLiking.save()

    elif request.method == "PUT" and userLiking not in [i.username for i in postLiking.likes.all()]:
        postLiking.likes.add(userLiking)
        postLiking.save()

@csrf_exempt
def index(request):
    
    likebutton(request, request.user, request.body)
    
    if request.method == "POST":

        newPost = Post(user=request.user, content=request.POST["content"])
        newPost.save()
    
    allPosts = Post.objects.all().order_by("-timestamp")
    p = Paginator(allPosts, 10)
    page_num = request.GET.get("page", 1)
    page = p.page(page_num)
    return render(request, "network/index.html", {
        "allPosts": page,
        "usuario": request.user,

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
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@csrf_exempt
def followingPosts(request):

    likebutton(request, request.user, request.body)

    user = User.objects.get(username=request.user)
    userFollowing = [user.username for user in user.following.all()]
    
    allPosts = Post.objects.filter(user__username__in=userFollowing).order_by("-timestamp").exclude(user__username=request.user)
    p = Paginator(allPosts, 10)
    page_num = request.GET.get("page", 1)
    page = p.page(page_num)

    return render(request, "network/following.html", {
        "FollowingPosts": page,
    })

@csrf_exempt
def profile(request, usuario):

    likebutton(request, request.user, request.body)

    requestUser = User.objects.get(username=request.user)
    newFollow = User.objects.get(username=usuario)
    if request.method == "POST" and usuario not in [u.username for u in requestUser.following.all()]:
        requestUser.following.add(newFollow)
        requestUser.save()
    elif request.method == "POST" and usuario in [u.username for u in requestUser.following.all()] : 
        requestUser.following.remove(newFollow)
        requestUser.save()

    allPosts = Post.objects.filter(user__username=usuario).order_by("-timestamp")
    p = Paginator(allPosts, 10)
    page_num = request.GET.get("page", 1)
    page = p.page(page_num)

    followButton = ""
    if usuario not in [u.username for u in requestUser.following.all()]:
        followButton = "Follow"
    else:
        followButton = "Unfollow"

    return render(request, "network/profile.html", {
        "profilePosts": page,
        "usersFollowing": newFollow.following.all(),
        "usersFollowers": newFollow.followers.all(),
        "userProfile": newFollow,
        "activeUserProfile": request.user,
        "followButton": followButton,
    })
    
@csrf_exempt
@login_required
def editPost(request, post_id):
    try:
        post = Post.objects.get(pk=post_id, user=request.user)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found"})
    
    if request.method == "PUT":
        data = json.loads(request.body)
        post.content = data["content"]
        post.save()
        return HttpResponse(status=204)