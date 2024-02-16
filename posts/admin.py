from django.contrib import admin
from .models import Post

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'public', 'classroom', 'author', 'hits', 'created_at']
    list_display_links = ['title']
    list_filter = ['public']
    search_fields = ['id', 'title', 'author__username']
    raw_id_fields = ['topic', 'classroom', 'author']

admin.site.register(Post, PostAdmin)