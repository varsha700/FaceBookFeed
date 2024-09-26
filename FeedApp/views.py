
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Message, Comment, Like
from django.http import JsonResponse

#FeedApp Home method
def  SHome(req):
    UserName= "User"    
    return render(req,"index.html",{"name":UserName})
    
# Register method
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('feed')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserCreationForm()
    return render(request,'register.html', {'form': form})

# FeedApp View
@login_required
def feed_view(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        image = request.FILES.get('image') 
        Message.objects.create(user=request.user, content=content, image=image)
        return redirect('feed')
    
    messages = Message.objects.prefetch_related('comments', 'likes').all()

    for message in messages:
        message.user_has_liked = message.likes.filter(user=request.user).exists()

    return render(request,'feed.html', {'messages': messages})

#Post comment method
@login_required
def post_comment(request, message_id):
    if request.method == 'POST':
        content = request.POST.get('content')
        message = get_object_or_404(Message, id=message_id)
        Comment.objects.create(user=request.user, message=message, content=content)
        return redirect('feed')

#Delete comment method
@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.user == request.user:
        comment.delete()
    return redirect('feed')

# Like Message method
@login_required
def like_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    liked = Like.objects.filter(user=request.user, message=message).exists()

    if liked:
        Like.objects.filter(user=request.user, message=message).delete()
    else:
        Like.objects.create(user=request.user, message=message)

    return redirect('feed')


# Delete Message method
@login_required
def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if message.user == request.user:
        message.delete()
    return redirect('feed')

# Login method
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('feed')
    else:
        form = AuthenticationForm()
    return render(request,'login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def toggle_like(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    like, created = Like.objects.get_or_create(user=request.user, message=message)
    
    if not created:
        like.delete()
    
    return redirect('feed')


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Message, id=post_id)
    if post.user == request.user:
        post.delete()
    return redirect('feed')

