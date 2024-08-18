from . import views
from django.urls import path


urlpatterns = [
     path('', views.PostList.as_view(), name='home'),
     path('category/<category>/', views.CatListView.as_view(),
          name='category'),
     path('add_post/', views.AddPostView.as_view(), name='add_post'),
     path('blog/<slug:slug>/', views.post_detail.as_view(), name='post_detail'),
     path('blog/<slug:slug>/edit_comment/<int:comment_id>', views.comment_edit, name='comment_edit'),
     path('blog/<slug:slug>/delete_comment/<int:comment_id>',
         views.comment_delete, name='comment_delete'),
     path('like/<slug:slug>', views.PostLike.as_view(), name='post_like'),
]