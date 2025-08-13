from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_post, name='create_post'),
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),   # ✅ Add custom login
    path('logout/', views.custom_logout, name='logout'),  # ✅ Custom logout
    #path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('posts/', views.all_posts, name='all_posts'),
]
