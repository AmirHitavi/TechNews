import pytest
from rest_framework.exceptions import ValidationError

from ..serializers import (
    NewsCreateInputSerializer,
    NewsDetailsInputSerializer,
    NewsDetailsOutputSerializer,
    NewsOutputSerializer,
    TagDetailsOutputSerializer,
    TagInputSerializer,
    TagOutputSerializer,
)
from .factories import NewsFactory, TagsFactory


@pytest.mark.django_db
class TestTagsSerializers:
    def test_tag_input_serializer(self):
        data = {"title": "Tech"}
        deserializer = TagInputSerializer(data=data)
        assert deserializer.is_valid()
        assert deserializer.validated_data["title"] == data["title"]

    def test_tag_output_serializer(self):
        tag = TagsFactory()
        serializer = TagOutputSerializer(tag)

        assert set(serializer.data.keys()) == {"id", "title"}
        assert serializer.data.get("id")
        assert serializer.data["title"] == tag.title

    def test_tag_output_serializer_with_multiple_tags(self):
        tags = TagsFactory.create_batch(5)
        serializer = TagOutputSerializer(tags, many=True)

        assert len(serializer.data) == 5

        for i in range(len(serializer.data)):
            tag = tags[i]
            assert set(serializer.data[i].keys()) == {"id", "title"}
            assert serializer.data[i].get("id")
            assert serializer.data[i].get("title") == tag.title

    def test_tag_details_output_serializer(self):
        tag = TagsFactory()
        serializer = TagDetailsOutputSerializer(tag)

        assert set(serializer.data.keys()) == {"id", "title", "created_at"}
        assert serializer.data.get("id")
        assert serializer.data.get("title") == tag.title
        assert serializer.data.get("created_at")


@pytest.mark.django_db
class TestNewsSerializers:

    def test_news_input_serializer(self):
        tags = TagsFactory.create_batch(5)
        tags_title = [tag.title for tag in tags]

        data = {
            "title": "test title",
            "content": "test content",
            "source": "test source",
            "is_public": True,
            "tags": tags_title,
        }

        deserializer = NewsCreateInputSerializer(data=data)
        assert deserializer.is_valid()
        assert deserializer.validated_data.get("title") == data.get("title")
        assert deserializer.validated_data.get("content") == data.get("content")
        assert deserializer.validated_data.get("source") == data.get("source")
        assert deserializer.validated_data.get("is_public") == data.get("is_public")
        assert deserializer.validated_data.get("tags") == data.get("tags")

    def test_news_input_serializer_without_is_public(self):
        tags = TagsFactory.create_batch(5)
        tags_title = [tag.title for tag in tags]

        data = {
            "title": "test title",
            "content": "test content",
            "source": "test source",
            "tags": tags_title,
        }

        deserializer = NewsCreateInputSerializer(data=data)
        assert deserializer.is_valid()
        assert deserializer.validated_data.get("title") == data.get("title")
        assert deserializer.validated_data.get("content") == data.get("content")
        assert deserializer.validated_data.get("source") == data.get("source")
        assert deserializer.validated_data.get("is_public")
        assert deserializer.validated_data.get("tags") == data.get("tags")

    def test_news_input_serializer_empty(self):

        data = {}

        with pytest.raises(ValidationError):
            deserializer = NewsCreateInputSerializer(data=data)
            deserializer.is_valid(raise_exception=True)

    def test_news_output_serializer(self):
        news = NewsFactory.create_batch(5)

        serializer = NewsOutputSerializer(news, many=True)

        assert len(serializer.data) == 5

        for i in range(len(serializer.data)):
            news_instance = news[i]
            data = serializer.data[i]
            expected_tags = [
                {"id": str(tag["id"]), "title": tag["title"]}
                for tag in news_instance.tags.values("id", "title")
            ]
            assert set(data.keys()) == {
                "id",
                "title",
                "source",
                "is_public",
                "tags",
            }

            assert data.get("id")
            assert data.get("title") == news_instance.title
            assert data.get("source") == news_instance.source
            assert data.get("is_public") == news_instance.is_public
            assert data.get("tags") == expected_tags

    def test_news_details_input_serializer(self):
        tags = TagsFactory.create_batch(5)
        tags_title = [tag.title for tag in tags]

        data = {
            "title": "test title",
            "content": "test content",
            "source": "test source",
            "is_public": True,
            "tags": tags_title,
        }

        deserializer = NewsDetailsInputSerializer(data=data)
        assert deserializer.is_valid()
        assert deserializer.validated_data.get("title") == data.get("title")
        assert deserializer.validated_data.get("content") == data.get("content")
        assert deserializer.validated_data.get("source") == data.get("source")
        assert deserializer.validated_data.get("is_public") == data.get("is_public")
        assert deserializer.validated_data.get("tags") == data.get("tags")

    def test_news_details_input_serializer_without_some_fields(self):
        tags = TagsFactory.create_batch(5)
        tags_title = [tag.title for tag in tags]

        data = {
            "title": "test title",
            "content": "test content",
            "tags": tags_title,
        }

        deserializer = NewsDetailsInputSerializer(data=data)
        assert deserializer.is_valid()
        assert deserializer.validated_data.get("title") == data.get("title")
        assert deserializer.validated_data.get("content") == data.get("content")
        assert deserializer.validated_data.get("tags") == data.get("tags")

    def test_news_details_input_serializer_empty(self):

        data = {}

        deserializer = NewsDetailsInputSerializer(data=data)
        assert deserializer.is_valid()

    def test_news_details_output_serializer(self):
        news = NewsFactory()
        serializer = NewsDetailsOutputSerializer(news)
        expected_tags = [
            {"id": str(tag["id"]), "title": tag["title"]}
            for tag in news.tags.values("id", "title")
        ]

        data = serializer.data

        assert set(data.keys()) == {
            "id",
            "title",
            "content",
            "source",
            "is_public",
            "tags",
            "estimated_reading_time",
            "created_at",
            "updated_at",
        }

        assert data.get("id")
        assert data.get("title") == news.title
        assert data.get("content") == news.content
        assert data.get("source") == news.source
        assert data.get("is_public") == news.is_public
        assert data.get("tags") == expected_tags
        assert data.get("estimated_reading_time") == news.estimated_reading_time
