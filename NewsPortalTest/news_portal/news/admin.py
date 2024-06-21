from django.contrib import admin
from .models import Category, Post
from django.urls import path, include


admin.site.register(Category)
admin.site.register(Post)

urlpatterns = [
   path('admin/', admin.site.urls),
   path('news/', include('news.urls')),
]

# Register your models here.
