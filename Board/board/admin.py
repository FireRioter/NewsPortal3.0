from django.contrib import admin
from .models import Ad, Response

@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'user', 'created_at']
    search_fields = ['title', 'content']
    list_filter = ['category']

@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ['ad', 'user', 'created_at', 'is_accepted']
    search_fields = ['content']