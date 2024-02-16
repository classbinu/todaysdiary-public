from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'nickname', 'email', 'point']
    list_display_links = ['username']
    # list_filter = []
    search_fields = ['id', 'username', 'nickname', 'email']
    filter_horizontal = ['blacklist']

admin.site.register(User, UserAdmin)