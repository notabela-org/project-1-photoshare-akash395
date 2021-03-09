from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from users.models import *
from .forms import *
from django.core.paginator import Paginator
from django.http import Http404

# Create your views here.
@login_required
def index(request):
    home = []
    posts = Post.objects.all()
    for post in posts:
        homeItem = {}
        homeItem['post'] =post
        try:
            homeItem['profile'] = Profile.objects.get(user = post.user)
            homeItem['comments'] = Comment.objects.filter(post = post)

        except ObjectDoesNotExist:
            print("Couldn't retrive profile or comments")
        home.append(homeItem)

    paginator = Paginator(home, 10)

    page_number = request.GET.get('page')
    page_obj    = paginator.get_page(page_number)
    return render(request, 'feed/index.html', {'page_obj': page_obj})


@login_required
def post(request,id):
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            cleanForm = form.cleaned_data
            user = request.user
            post = Post.objects.get(id=id)
            comment = Comment(user=user,post=post,comment=cleanForm['comment'])
            comment.save()

            return HttpResponseRedirect(reverse('index'))
        return render(request,'feed/post.html',{'id':id,'form':form})

    homeItem = {}
    try:
        post = Post.objects.get(id=id)
        homeItem['post'] = post
        homeItem['profile'] = Profile.objects.get(user=post.user)
        homeItem['comments'] = []
        comments = list(Comment.objects.filter(post=post))
        for item in comments:
            commentDict = {'comment':item}
            profile = Profile.objects.get(user=item.user)
            commentDict['profile'] = profile
            homeItem['comments'].append(commentDict)
    except ObjectDoesNotExist:
        print("Failed to fetch profile or comments")
        homeItem['comments'] = []

    return render(request,'feed/post.html',{'id':id,'form':form,'homeItem':homeItem})


@login_required
def profile(request,username):
    try:
        user = User.objects.get(username=username)
        profile = Profile.objects.get(user=user)
    except ObjectDoesNotExist:
        profile = None
    return render(request, 'feed/profile.html', {'profile':profile,'username':user.get_username()})

@login_required
def editprofile(request):
    
    form = None
    if request.method == 'POST':
        form = EditProfileForm(data=request.POST,files=request.FILES)

        if form.is_valid():
            cleanForm = form.cleaned_data
            user = User.objects.get(username=request.user.get_username())
            user.username = cleanForm['username']
            user.save()
            profile = Profile(user=user,bio=cleanForm['bio'],image=cleanForm['image'])
            profile.save()
            return HttpResponseRedirect(reverse('index'))

        return render(request, 'feed/editprofile.html',{'form':form})

    try:
        user = User.objects.get(username=request.user.get_username())
        profile = Profile.objects.get(user=user)
        form = EditProfileForm(data={'username':user.get_username(),'bio':profile.get_bio(),'image':profile.get_image()})
    except ObjectDoesNotExist:
        form = EditProfileForm(data={'username':request.user.get_username()})
    return render(request, 'feed/editprofile.html',{'form':form})


@login_required
def newpost(request):
    form = NewPostForm()
    if request.method == 'POST':
        form = NewPostForm(data=request.POST, files= request.FILES)
        if form.is_valid():
            cleanForm = form.cleaned_data
            post = Post(user= request.user, image=cleanForm['image'],caption=cleanForm['caption'])
            post.save()

            return HttpResponseRedirect(reverse('index'))
        return render(request,'feed/newpost.html',{'form': form})
    return render(request,'feed/newpost.html',{'form': form})