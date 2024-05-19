from django.contrib import admin
from .models import News

# Register your models here.
class NewsAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['title', 'content', 'display']}),
    ]

    list_display = ['title', 'date_posted', 'display']
    list_filter = ['date_posted', 'display']
    search_fields = ['title', 'content']

admin.site.register(News, NewsAdmin)