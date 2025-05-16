from django.urls import path

from blog import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('category/<slug:category_slug>/',
         views.category_posts, name='category_posts'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('posts/create/', views.create_post, name='create_post'),
]
