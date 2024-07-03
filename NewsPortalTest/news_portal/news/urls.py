from django.urls import path
from .views import (PostList, PostDetail, PostFilterView, create_post,
                    edit_post, delete_post)


urlpatterns = [
   path('', PostList.as_view(), name='posts'),
   path('<int:pk>/', PostDetail.as_view(), name='post'),
   path('search/', PostFilterView.as_view()),
   path('create/', create_post,name='Create post'),
   path('<int:pk>/edit/',edit_post, name='Update post'),
   path('<int:pk>/delete/', delete_post, name='Delete'),
]