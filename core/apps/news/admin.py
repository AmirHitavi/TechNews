from django.contrib import admin

from .models import News, Tags

# Register your models here.


@admin.register(Tags)
class AdminTags(admin.ModelAdmin):
    list_display = ["title", "created_at"]
    search_fields = ["title"]
    ordering = ["-created_at"]


@admin.register(News)
class AdminNews(admin.ModelAdmin):
    list_display = ["title", "source", "is_public", "created_at", "updated_at"]
    list_editable = ["is_public"]
    list_filter = ["tags"]
    search_fields = ["title", "tags__title"]
    search_help_text = "Search for News via 'title', 'tags'"
    ordering = ["-created_at", "-updated_at"]
