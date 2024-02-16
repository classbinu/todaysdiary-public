from django.contrib import admin
from .models import Classroom


# Register your models here.

class ClassroomAdmin(admin.ModelAdmin):
    list_display = ['id', 'year', 'school', 'grade', 'number', 'teacher', 'state']
    list_display_links = ['school']
    list_filter = ['grade']
    search_fields = ['id', 'school', 'teacher__username']
    raw_id_fields = ['teacher']
    filter_horizontal = ['student']


admin.site.register(Classroom, ClassroomAdmin)