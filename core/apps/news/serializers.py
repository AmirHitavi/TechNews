from rest_framework import serializers

from .models import News, Tags


class TagInputSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, max_length=100)


class TagOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ["id", "title"]
        read_only_fields = ["title"]


class TagDetailsOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ["id", "title", "created_at"]
        read_only_fields = ["id", "created_at"]


class NewsCreateInputSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100, required=True)
    content = serializers.CharField(required=True)
    source = serializers.CharField(max_length=50, required=True)
    is_public = serializers.BooleanField(default=True)
    tags = serializers.ListField(
        child=serializers.CharField(max_length=100), required=True
    )


class NewsOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = [
            "id",
            "title",
            "source",
            "is_public",
            "slug",
            "tags",
        ]
        read_only_fields = ["id", "slug"]


class NewsDetailsInputSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100, required=False)
    content = serializers.CharField(required=False)
    source = serializers.CharField(max_length=50, required=False)
    is_public = serializers.BooleanField(required=False)
    tags = serializers.ListField(
        child=serializers.CharField(max_length=100), required=False, default=list
    )


class NewsDetailsOutputSerializer(serializers.ModelSerializer):
    estimated_reading_time = serializers.SerializerMethodField()

    class Meta:

        model = News
        fields = [
            "id",
            "title",
            "content",
            "source",
            "is_public",
            "slug",
            "tags",
            "estimated_reading_time",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "slug", "created_at", "updated_at"]

    def get_estimated_reading_time(self, obj):
        return obj.estimated_reading_time
