from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.SHome, name='home'),
    path('register/', views.register, name='register'),
    path('feed/', views.feed_view, name='feed'),
    path('post_comment/<int:message_id>/', views.post_comment, name='post_comment'),
    path('like_message/<int:message_id>/', views.like_message, name='like_message'),
    path('delete_message/<int:message_id>/', views.delete_message, name='delete_message'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('toggle_like/<int:message_id>/', views.toggle_like, name='toggle_like'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
