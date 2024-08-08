from . import views
from django.urls import path


urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
     path('category/<category>/', views.CatListView.as_view(),
          name='category'),
    path('add_category/', views.AddCategoryView.as_view(), name='add_category'),
    path('<slug:slug>/', views.post_detail.as_view(), name='post_detail'),
    path('<slug:slug>/edit_comment/<int:comment_id>', views.comment_edit, name='comment_edit'),
    path('<slug:slug>/delete_comment/<int:comment_id>',
         views.comment_delete, name='comment_delete'),
    path('like/<slug:slug>', views.PostLike.as_view(), name='post_like'),
]