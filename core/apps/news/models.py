from autoslug import AutoSlugField
from django.db import models
from django.utils import timezone

from .read_time_engine import NewsReadTimeEngine

# Create your models here.


class Tags(models.Model):
    title = models.CharField(max_length=100, unique=True, null=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title.title()


class News(models.Model):
    title = models.CharField(max_length=100, null=False)
    content = models.TextField(null=False)
    source = models.CharField(max_length=50, null=False)
    is_public = models.BooleanField(null=False, default=True)
    slug = AutoSlugField(populate_from="title", always_update=True, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tags, related_name="news")

    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"
        ordering = ["-updated_at", "-created_at"]

    def __str__(self):
        return self.title.title()

    @property
    def estimated_reading_time(self):
        return NewsReadTimeEngine.estimate(self)
