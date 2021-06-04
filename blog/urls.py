from django.urls import path
from . import views
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView, \
    LikeView, CommentCreateView, OldListView, FamousListView

urlpatterns = [
    path('like/<int:pk>', LikeView, name="like_post"),
    path('', PostListView.as_view(), name='blog-home'),
    path('old', OldListView.as_view(), name='old_blog-home'),
    path('most-liked', FamousListView.as_view(), name='most_liked_blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('about/', views.about, name='blog-about'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/comment/', CommentCreateView.as_view(), name='add_comment'),
    path('search/', views.SearchPage, name='search_result'),

]
