from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views 
from moj_app import views 
from moj_app.views import (
    PostListView, 
    PostDetailView, 
    PostCreateView, 
    PostUpdateView, 
    PostDeleteView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('', PostListView.as_view(), name='post_list'), 
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='post_edit'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    
    path('post/<int:pk>/like/', views.like_post, name='like_post'),
]