from django.contrib import admin
from .models import Topic

# Register your models here.

class TopicAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'public']
    list_display_links = ['title']
    # list_filter = []
    search_fields = ['id', 'title', 'public']


admin.site.register(Topic, TopicAdmin)