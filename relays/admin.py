from django.contrib import admin
from .models import Relay


class RelayAdmin(admin.ModelAdmin):
    list_display = ['id', 'post', 'public', 'status', 'created_at']
    list_display_links = ['post']
    list_filter = ['public', 'status']
    search_fields = ['id', 'post']
    raw_id_fields = ['post']

admin.site.register(Relay, RelayAdmin)