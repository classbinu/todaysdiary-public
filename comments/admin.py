from django.contrib import admin
from .models import Comment

# Register your models here.

class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'content', 'author', 'public', 'created_at']
    list_display_links = ['content']
    # list_filter = []
    search_fields = ['id', 'content', 'author__username']
    raw_id_fields = ['post', 'author']


admin.site.register(Comment, CommentAdmin)