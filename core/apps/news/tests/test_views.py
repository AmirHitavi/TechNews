import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APIRequestFactory

from ..models import News
from ..serializers import (
    NewsCreateInputSerializer,
    NewsDetailsInputSerializer,
    NewsDetailsOutputSerializer,
    NewsOutputSerializer,
    TagDetailsOutputSerializer,
    TagInputSerializer,
    TagOutputSerializer,
)
from ..views import NewsApi, NewsDetailsApi, TagsApi, TagsDetailsApi
from .factories import NewsFactory, TagsFactory


@pytest.mark.django_db
class TestTagsApi:
    client = APIClient()
    url = reverse("tag-create-get")

    def test_tags_api_get(self):
        tags = list(reversed(TagsFactory.create_batch(5)))

        response = self.client.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data.get("count") == 5
        assert response.data.get("results")

        for i in range(response.data.get("count")):
            tag = tags[i]
            result = response.data.get("results")[i]
            assert result.get("id") == tag.id
            assert result.get("title") == tag.title

    def test_tags_api_get_empty(self):
        response = self.client.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data.get("count") == 0
        assert response.data.get("results") == []

    def test_tags_api_post_valid(self):
        data = {"title": "Tech"}
        response = self.client.post(self.url, data=data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data.get("id")
        assert response.data.get("title") == data.get("title")

    def test_tags_api_post_invalid(self):

        empty_data = {}

        response = self.client.post(self.url, data=empty_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        invalid = {"id": 1, "title": "Tech"}

        response = self.client.post(self.url, data=invalid)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_tags_api_post_duplicate(self):
        data = {"title": "Tech"}
        response = self.client.post(self.url, data=data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data.get("id")
        assert response.data.get("title") == data.get("title")

        response = self.client.post(self.url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_tags_api_get_serializer_class(self):
        factory = APIRequestFactory()
        view = TagsApi()

        post_request = factory.post(self.url, data={"title": "Tech"})
        view.request = post_request
        serializer_class = view.get_serializer_class()
        assert serializer_class == TagInputSerializer

        get_request = factory.get(self.url)
        view.request = get_request
        serializer_class = view.get_serializer_class()
        assert serializer_class == TagOutputSerializer

    def test_tags_api_invalid_method(self):

        response = self.client.patch(self.url)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

        response = self.client.put(self.url)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

        response = self.client.delete(self.url)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.django_db
class TestTagsDetailsApi:
    client = APIClient()
    url_name = "tag-details"

    def test_tags_details_get(self):
        tag = TagsFactory()

        url = reverse(self.url_name, args=[tag.id])

        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == tag.id
        assert response.data["title"] == tag.title

    def test_tags_details_get_not_found(self):
        tag = TagsFactory()
        tag_id = tag.id
        tag.delete()

        url = reverse(self.url_name, args=[tag_id])

        response = self.client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_tags_details_put(self):
        tag = TagsFactory()
        url = reverse(self.url_name, args=[tag.id])
        data = {"title": "Update test"}

        response = self.client.put(url, data=data)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert response.data["id"] == tag.id
        assert response.data["title"] == data["title"]

    def test_tags_details_put_not_found(self):
        tag = TagsFactory()
        tag_id = tag.id
        tag.delete()

        url = reverse(self.url_name, args=[tag_id])
        data = {"title": "Update test"}

        response = self.client.put(url, data=data)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_tags_details_put_invalid_input(self):
        tag = TagsFactory()

        url = reverse(self.url_name, args=[tag.id])
        data = {"id": 1, "title": "Update test"}

        response = self.client.put(url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_tags_details_put_empty_input(self):
        tag = TagsFactory()

        url = reverse(self.url_name, args=[tag.id])
        data = {}

        response = self.client.put(url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_tags_details_delete(self):
        tag = TagsFactory()
        url = reverse(self.url_name, args=[tag.id])

        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_tags_details_delete_not_found(self):
        tag = TagsFactory()
        tag_id = tag.id
        tag.delete()
        url = reverse(self.url_name, args=[tag_id])

        response = self.client.delete(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_tags_details_get_serializer_class(self):
        factory = APIRequestFactory()
        view = TagsDetailsApi()

        tag = TagsFactory()
        tag_id = tag.id
        url = reverse(self.url_name, args=[tag_id])

        put_request = factory.put(url, data={"title": "Update test"})
        view.request = put_request
        serializer_class = view.get_serializer_class()
        assert serializer_class == TagInputSerializer

        get_request = factory.get(url)
        view.request = get_request
        serializer_class = view.get_serializer_class()
        assert serializer_class == TagDetailsOutputSerializer

    def test_tags_details_invalid_method(self):
        tag = TagsFactory()
        url = reverse(self.url_name, args=[tag.id])

        response = self.client.patch(url)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

        response = self.client.post(url)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.django_db
class TestNewsApi:
    client = APIClient()
    url = reverse("news-create-get")

    def test_news_api_get(self):
        news = list(reversed(NewsFactory.create_batch(5)))

        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get("count") == 5
        assert response.data.get("results")

        for i in range(len(response.data.get("results"))):
            news_instance = news[i]
            data = response.data.get("results")[i]
            assert data.get("id") == news_instance.id
            assert data.get("title") == news_instance.title
            assert data.get("is_public") == news_instance.is_public
            assert data.get("slug") == news_instance.slug
            assert data.get("tags") == list(news_instance.tags.values("id", "title"))

    def test_news_api_get_empty(self):
        response = self.client.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data.get("count") == 0
        assert response.data.get("results") == []

    def test_news_api_post(self):
        tags = TagsFactory.create_batch(5)
        tags_title = [tag.title for tag in tags]

        data = {
            "title": "test title",
            "content": "test content",
            "source": "test source",
            "is_public": True,
            "tags": tags_title,
        }

        response = self.client.post(self.url, data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data.get("id")
        assert response.data.get("title") == data.get("title")
        assert response.data.get("source") == data.get("source")
        assert response.data.get("is_public") == data.get("is_public")
        assert (
            response.data.get("tags")
            == [{"id": tag.id, "title": tag.title} for tag in tags][::-1]
        )

    def test_news_api_post_invalid_input(self):

        empty = {}

        response = self.client.post(self.url, data=empty)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        tags = TagsFactory.create_batch(5)
        tags_title = [tag.title for tag in tags]

        invalid_data = {
            "id": 1,
            "title": "test title",
            "content": "test content",
            "source": "test source",
            "is_public": True,
            "tags": tags_title,
        }

        response = self.client.post(self.url, data=invalid_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_news_api_get_serializer_class(self):
        factory = APIRequestFactory()
        view = NewsApi()

        tags = TagsFactory.create_batch(5)
        tags_title = [tag.title for tag in tags]

        data = {
            "title": "test title",
            "content": "test content",
            "source": "test source",
            "is_public": True,
            "tags": tags_title,
        }
        post_request = factory.post(self.url, data=data)
        view.request = post_request
        serializer_class = view.get_serializer_class()
        assert serializer_class == NewsCreateInputSerializer

        get_request = factory.get(self.url)
        view.request = get_request
        serializer_class = view.get_serializer_class()
        assert serializer_class == NewsOutputSerializer

    def test_news_api_invalid_method(self):

        response = self.client.patch(self.url)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

        response = self.client.put(self.url)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

        response = self.client.delete(self.url)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.django_db
class TestNewsDetailsApi:
    client = APIClient()
    url_name = "news-details"

    def test_news_details_get(self):
        news = NewsFactory()
        url = reverse(self.url_name, args=[news.slug])

        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get("id") == news.id
        assert response.data.get("title") == news.title
        assert response.data.get("content") == news.content
        assert response.data.get("source") == news.source
        assert response.data.get("is_public") == news.is_public
        assert response.data.get("slug") == news.slug
        assert response.data.get("tags") == list(news.tags.values("id", "title"))
        assert (
            response.data.get("estimated_reading_time") == news.estimated_reading_time
        )
        assert response.data.get("created_at")
        assert response.data.get("updated_at")

    def test_news_details_get_not_found(self):
        news = NewsFactory()
        news_slug = news.slug
        news.delete()

        url = reverse(self.url_name, args=[news_slug])
        response = self.client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_news_details_put(self):
        news = NewsFactory()
        url = reverse(self.url_name, args=[news.slug])

        tags = TagsFactory.create_batch(5)
        tags_title = [tag.title for tag in tags]

        data = {
            "title": "test title",
            "content": "test content",
            "source": "test source",
            "is_public": True,
            "tags": tags_title,
        }

        response = self.client.put(url, data=data)

        assert response.data.get("slug")
        new_slug = response.data.get("slug")

        news = News.objects.get(slug=new_slug)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert response.data.get("id") == news.id
        assert response.data.get("title") == news.title

    def test_news_details_put_empty(self):
        news = NewsFactory()
        url = reverse(self.url_name, args=[news.slug])

        data = {}

        response = self.client.put(url, data=data)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert response.data.get("slug")

        new_slug = response.data.get("slug")
        news = News.objects.get(slug=new_slug)

        assert response.data.get("id") == news.id
        assert response.data.get("title") == news.title

    def test_news_details_put_not_found(self):
        news = NewsFactory()
        news_slug = news.slug
        news.delete()

        url = reverse(self.url_name, args=[news_slug])

        tags = TagsFactory.create_batch(5)
        tags_title = [tag.title for tag in tags]

        data = {
            "title": "test title",
            "content": "test content",
            "source": "test source",
            "is_public": True,
            "tags": tags_title,
        }

        response = self.client.put(url, data=data)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_news_details_put_invalid_input(self):
        news = NewsFactory()
        url = reverse(self.url_name, args=[news.slug])

        tags = TagsFactory.create_batch(5)
        tags_title = [tag.title for tag in tags]

        data = {
            "id": 1,
            "title": "test title",
            "content": "test content",
            "source": "test source",
            "is_public": True,
            "tags": tags_title,
        }

        response = self.client.put(url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_news_details_put_not_found_tags(self):
        news = NewsFactory()
        url = reverse(self.url_name, args=[news.slug])

        data = {
            # not exists
            "tags": ["tag1"],
        }

        response = self.client.put(url, data=data)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_news_details_delete(self):
        news = NewsFactory()
        url = reverse(self.url_name, args=[news.slug])

        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_news_details_delete_not_found(self):
        news = NewsFactory()
        news_slug = news.slug
        news.delete()
        url = reverse(self.url_name, args=[news_slug])

        response = self.client.delete(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_news_details_get_serializer_class(self):
        factory = APIRequestFactory()
        view = NewsDetailsApi()

        news = NewsFactory()
        news_slug = news.slug
        url = reverse(self.url_name, args=[news_slug])

        tags = TagsFactory.create_batch(5)
        tags_title = [tag.title for tag in tags]

        data = {
            "title": "test title",
            "content": "test content",
            "source": "test source",
            "is_public": True,
            "tags": tags_title,
        }

        put_request = factory.put(url, data=data)
        view.request = put_request
        serializer_class = view.get_serializer_class()
        assert serializer_class == NewsDetailsInputSerializer

        get_request = factory.get(url)
        view.request = get_request
        serializer_class = view.get_serializer_class()
        assert serializer_class == NewsDetailsOutputSerializer

    def test_tags_details_invalid_method(self):
        news = NewsFactory()
        url = reverse(self.url_name, args=[news.slug])

        response = self.client.patch(url)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

        response = self.client.post(url)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
