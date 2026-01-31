from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm

# 1. REGISTRACIJA
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login') # Nakon reg. šalji na login
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# 2. LISTA POSTOVA (Naslovnica)
def post_list(request):
    posts = Post.objects.all().order_by('-created_at') # Najnoviji prvi
    return render(request, 'posts/post_list.html', {'posts': posts})

# 3. DETALJI POSTA
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'posts/post_detail.html', {'post': post})

# 4. KREIRANJE POSTA (Samo za logirane)
@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user # Automatski dodaj autora
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'posts/post_form.html', {'form': form})