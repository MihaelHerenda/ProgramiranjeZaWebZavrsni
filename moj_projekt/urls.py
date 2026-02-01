from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views 
from moj_app import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # AUTH 
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # POST 
    path('', views.post_list, name='post_list'), 
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_create, name='post_create'),

    path('post/<int:pk>/like/', views.like_post, name='like_post'),

    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
]