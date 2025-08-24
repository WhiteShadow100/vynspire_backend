from django.contrib import admin
from django.urls import path, include
from blog import views as blog_views
from account import views as account_views


urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('register/', account_views.register, name ="Register"),
    path('login/', account_views.login, name = "Register"),
    path("posts/", blog_views.manage_post, name="Manages All Post Endpoint"),
    path("posts/<int:post_id>/", blog_views.manage_post, name="Manages All Post Endpoint"),
]
