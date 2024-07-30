from django.urls import path,include
from .views import (PostList, PostDetail, PostFilterView, create_post,
                    edit_post, delete_post)
from django.contrib import admin
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView


urlpatterns = [
   path('', PostList.as_view(), name='posts'),
   path('<int:pk>/', PostDetail.as_view(), name='post'),
   path('search/', PostFilterView.as_view()),
   path('create/', create_post,name='Create post'),
   path('<int:pk>/edit/',edit_post, name='Update post'),
   path('<int:pk>/delete/', delete_post, name='Delete'),
   path('admin/', admin.site.urls),
   path('accounts/', include('allauth.urls')),
   path('swagger-ui/', TemplateView.as_view(
       template_name='swagger-ui.html',
       extra_context={'schema_url':'openapi-schema'}
   ), name='swagger-ui'),
]