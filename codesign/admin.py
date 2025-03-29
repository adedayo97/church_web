# codesign/admin.py
from django.contrib import admin
from .models import SliderImage, AboutImage, ServiceImage, VideoImage, TeamImage, BlogImage,Event
from tinymce.widgets import TinyMCE
from django.db import models
from .models import Event

@admin.register(SliderImage)
class SliderImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title',)
    list_per_page = 20

@admin.register(AboutImage)
class AboutImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title',)
    list_per_page = 20

@admin.register(ServiceImage)
class ServiceImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'created_at')  # Added subtitle for clarity
    search_fields = ('title', 'subtitle')
    list_per_page = 20

@admin.register(VideoImage)
class VideoImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'youtube_url', 'created_at')  # Added youtube_url
    search_fields = ('title', 'youtube_url')
    list_per_page = 20
    list_filter = ('created_at',)  # Optional: filter by creation date
    fields = ('title', 'image', 'youtube_url')  # Explicitly show fields in edit form

@admin.register(TeamImage)
class TeamImageAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'created_at')
    search_fields = ('name', 'position')
    list_per_page = 20

@admin.register(BlogImage)
class BlogImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'post_date', 'created_at')
    list_filter = ('post_date', 'author')
    search_fields = ('title', 'description', 'full_content')
    fields = ('title', 'image', 'description', 'full_content', 'scripture', 'prayer_points', 'post_date', 'author')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', )
    list_filter = ('category',)
    search_fields = ('title', 'description')
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }