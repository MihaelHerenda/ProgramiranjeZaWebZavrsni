from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views 
from moj_app import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # AUTH RUTE
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # POST RUTE
    path('', views.post_list, name='post_list'), # Naslovnica
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_create, name='post_create'),
]