from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Post, Like, Comment
from .forms import PostForm, CommentForm 
from django.db.models import Q


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def post_list(request):
    query = request.GET.get('q') # Dohvati ono što je upisano u tražilicu
    
    if query:
        # Filtriraj po naslovu ILI sadržaju
        posts = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        ).order_by('-created_at')
    else:
        posts = Post.objects.all().order_by('-created_at')
        
    return render(request, 'posts/post_list.html', {'posts': posts, 'query': query})

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'posts/post_form.html', {'form': form})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all() 
    
    is_liked = False
    if request.user.is_authenticated:
        if post.likes.filter(user=request.user).exists():
            is_liked = True

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login') 
            
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()

    return render(request, 'posts/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
        'is_liked': is_liked 
    })

@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    
    if not created:
        like.delete()
        
    return redirect('post_detail', pk=pk)

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
   
    if request.user != post.author:
        return redirect('post_detail', pk=pk)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post) 
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=pk)
    else:
        form = PostForm(instance=post)
    
    
    return render(request, 'posts/post_form.html', {'form': form, 'is_edit': True})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    if request.user == post.author:
        post.delete()
        
    return redirect('post_list')