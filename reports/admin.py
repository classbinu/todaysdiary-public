from django.contrib import admin
from .models import Report



class ReportAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'ref', 'content', 'state', 'created_at']
    list_display_links = ['type']
    list_filter = ['state', 'type']
    search_fields = ['id', 'type', 'content', 'author', 'state']
    raw_id_fields = ['author']


admin.site.register(Report, ReportAdmin)