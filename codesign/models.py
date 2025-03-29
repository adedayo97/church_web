# codesign/models.py
from django.db import models

class SliderImage(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)  # Optional
    image = models.ImageField(upload_to='slider_images/')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or f"Slider Image {self.id}"

class AboutImage(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)  # Optional
    image = models.ImageField(upload_to='about_images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or f"About Image {self.id}"

class ServiceImage(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    subtitle = models.CharField(max_length=100, blank=True, null=True)  # Ensure this exists
    image = models.ImageField(upload_to='service_images/')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or f"Service Image {self.id}"

class VideoImage(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='video_images/')
    youtube_url = models.URLField(max_length=200, blank=True, null=True)  # Add this if missing
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or f"Video Image {self.id}"

class TeamImage(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)  # Optional
    position = models.CharField(max_length=100, blank=True, null=True)  # Optional
    image = models.ImageField(upload_to='team_images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name or f"Team Image {self.id}"

class BlogImage(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='blog_images/')
    description = models.TextField(blank=True)
    full_content = models.TextField(blank=True, null=True)
    post_date = models.DateField()
    author = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    scripture = models.CharField(max_length=200, blank=True, null=True)  # New field
    prayer_points = models.TextField(blank=True, null=True)  # New field

    def __str__(self):
        return self.title or f"Blog Image {self.id}"
    

class Event(models.Model):
    CATEGORY_CHOICES = [
        ('weekly', 'Weekly Services'),
        ('monthly', 'Monthly Services'),
        ('deliverance', 'Deliverance'),
    ]

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='weekly')
    title = models.CharField(max_length=200)
    #date = models.CharField(max_length=100, blank=True, null=True)  # Make optional
    #time = models.CharField(max_length=50, blank=True, null=True)  # Make optional
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} ({self.get_category_display()})"

    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"