from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentCreateView, CommentListView, CategoryListView, CategoryPostListView, TagListView, TagPostListView

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='posts')

urlpatterns = [
    path('', include(router.urls)),
    path('posts/comments/', CommentCreateView.as_view(), name='comment-create'),
    path('posts/comments/', CommentListView.as_view(), name='comment-list'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/posts/<int:pk>/', CategoryPostListView.as_view(), name='category-posts'),
    path('tags/', TagListView.as_view(), name='tag-list'),
    path('tags/posts/<int:pk>/', TagPostListView.as_view(), name='tag-posts'),
]
