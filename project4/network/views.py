from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import json

from .models import User, Post,Follow, Comment
from .forms import PostForm

def index(request):
    user = None
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        authenticate = True
    else:
        authenticate = False
    
    form = PostForm()
    all_posts = Post.objects.order_by("-time").all()
    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get('page',1)
    page_obj = paginator.get_page(page_number)
    all_pages = list(paginator.get_elided_page_range(page_number, on_each_side=2, on_ends=0))
    return render(request, "network/index.html", {
        "form": form,
        "page_obj":page_obj,
        "all_pages":all_pages,
        "user":user,
        "authenticate":authenticate,
    })

    

def login_view(request):
    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

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

        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

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
def create(request):
    if request.method != "POST":
        return  JsonResponse({'error':'Method must be POST'}, status=400)
    form = PostForm(request.POST)
    if form.is_valid():
        user = User.objects.get(id=request.user.id)
        text = form.cleaned_data["text"]
        post = Post(
            text= text,
            publisher = user
        )
        post.save()
        return HttpResponseRedirect(reverse("index"))
    else: 
        return  JsonResponse({'error':'Post could not send!'}, status=400)
    
def user_page(request, username):
    try:
        page_user = User.objects.get(username=username)
    except User.DoesNotExist:
        return  JsonResponse({'error':'Post could not send!'}, status=404)
    try:
        user = User.objects.get(id=request.user.id)
    except User.DoesNotExist:
        user = None
    try:
        follow = Follow.objects.get(user=page_user)
    except:
        follow = Follow.objects.create(user=page_user)

    posts = Post.objects.filter(publisher=page_user).order_by("-time").all()
    return render(request, "network/user.html",{
        "user":user,
        "page_user":page_user,
        "posts":posts,
        "follow":follow,
    })

@login_required(login_url="network:login")
def following(request):
    try:
        user = User.objects.get(id=request.user.id)
    except User.DoesNotExist:
        return  JsonResponse({'error':'User Could not Found!'}, status=400)

    try:
        follow = Follow.objects.get(user=user)
    except Follow.DoesNotExist:
        follow = Follow.objects.create(user=user)

    post = Post.objects.filter(publisher__in=follow.follow.all())
    return render(request, "network/follows.html", {
        "posts":post,
        "user":user,
    })
    


@csrf_exempt
def like(request, post_id):
    if request.method != "POST":
        return  JsonResponse({'error':' Method Must be POST'}, status=400)
    
    if request.user.is_authenticated == False:  
        return  JsonResponse({'error':' User is not Authenticated'}, status=401)

    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return  JsonResponse({'error': 'Post Does Not Exist'})
    
    try:
        user = User.objects.get(id=request.user.id)
    except User.DoesNotExist:
        return  JsonResponse({'error':' User Does Not Exist'})

    if user in post.like.all():
        post.like.remove(user)
        return JsonResponse({"Unlike": "Success"}, status=200)
    else:
        post.like.add(user)
        return JsonResponse({"like": "Success"}, status=200)
    
@csrf_exempt
def follow(request, user1):
    if request.method != "POST":
        return  JsonResponse({'error':' Method Must be POST'}, status=400)
    
    if request.user.is_authenticated == False:
        return  JsonResponse({'error':' User is not Authenticated'}, status=401)
    
    try:
        user = User.objects.get(id=request.user.id)
    except User.DoesNotExist:
        return  JsonResponse({'error':' User is not Authenticated'}, status=401)
    
    try:
        page_user = User.objects.get(username=user1)
    except User.DoesNotExist:
        return  JsonResponse({'error':' User Could Not Found'}, status=400)
   
    try:
        page_follow = Follow.objects.get(user=page_user)
    except Follow.DoesNotExist:
        page_follow = Follow.objects.create(user=page_user)
        return  JsonResponse({'error':' Follow Could Not Found'}, status=400)

    
    try:
        follow = Follow.objects.get(user=user)
    except Follow.DoesNotExist:
        follow = Follow.objects.create(user=user)
        return  JsonResponse({'error':' Follow Could Not Found'}, status=400)

    if user in page_follow.follower.all():
        page_follow.follower.remove(user)
        follow.follow.remove(page_user)
        return JsonResponse({"unFollow": "Success"}, status=200)
    else:
        page_follow.follower.add(user)
        follow.follow.add(page_user)
        return JsonResponse({"follow": "Success"}, status=200)

@csrf_exempt
def edit(request,post_id):
    if request.user.is_authenticated:
        if request.method != "POST":
            return  JsonResponse({'error':' Method Must be POST'}, status=400)
            
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return  JsonResponse({'error':' Post Does Not Exist'}, status=400)
        
        data = json.loads(request.body)
        text = data['text']
        if text == "":
            return  JsonResponse({'error':' Text Can Not be Free'}, status=400)
        post.text = text
        post.save()
        return  JsonResponse({'succes':' User Does Not Auchenticated'}, status=200)
    else:
        return  JsonResponse({'error':' User Does Not Auchenticated'}, status=400)


def comment(request, post_id):
    try:
        user = User.objects.get(id=request.user.id)
    except User.DoesNotExist:
        user = None

    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return  JsonResponse({'error':' Post Does Not Exist'}, status=400)

    comments = Comment.objects.filter(post=post).order_by("-comment_time").reverse()

    return render(request, "network/post.html",{
        "user":user,
        "comments":comments,
        "post":post,
    })

@csrf_exempt
def add_comment(request, post_id):
    if request.method != "POST":
        return  JsonResponse({'error':' Method Must be POST'}, status=400)
    
    if request.user.is_authenticated == False:
        return  JsonResponse({'error':' User is not Authenticated'}, status=401)
    
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return  JsonResponse({'error':' Post Does Not Exist'}, status=400)

    user = User.objects.get(id=request.user.id)
    data = json.loads(request.body)
    text = data['text']
    if text == "":
        return JsonResponse({'error':' There Must be at Least 1 Character'}, status=400)

    comment = Comment.objects.create(
        owner=user,
        post=post,
        comment=text,
    )
    comment.save()
    return JsonResponse({"Comment": "Success", "user":user.username}, status=200)
