import uuid

from django.db import models
from django.utils import timezone

from .read_time_engine import NewsReadTimeEngine

# Create your models here.


class BaseModel(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, db_index=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True
        ordering = [
            "-created_at",
        ]


class Tags(BaseModel):
    title = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    def __str__(self):
        return self.title


class News(BaseModel):
    title = models.CharField(max_length=255, null=False)
    content = models.TextField(null=False)
    source = models.URLField(unique=True)
    tags = models.ManyToManyField(Tags, related_name="news")
    is_public = models.BooleanField(null=False, default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"
        ordering = ["-updated_at", "-created_at"]

    def __str__(self):
        return self.title

    @property
    def estimated_reading_time(self):
        return NewsReadTimeEngine.estimate(self)
