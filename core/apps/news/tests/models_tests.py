from math import ceil

import pytest

from ..read_time_engine import NewsReadTimeEngine
from .factories import NewsFactory, TagsFactory


@pytest.mark.django_db
def test_create_tag():
    tag = TagsFactory()
    assert tag is not None
    assert tag.id is not None
    assert tag.title is not None


@pytest.mark.django_db
def test_str_tag():
    tag = TagsFactory()
    assert str(tag) == tag.title.title()


@pytest.mark.django_db
def test_create_news():
    news = NewsFactory()
    assert news is not None
    assert news.id is not None
    assert news.title is not None
    assert news.content is not None
    assert news.source is not None
    assert news.slug is not None
    assert news.is_public is not None
    assert news.created_at is not None
    assert news.updated_at is not None
    assert news.tags is not None
    assert news.tags.count() == 5


@pytest.mark.django_db
def test_str_news():
    news = NewsFactory()
    assert str(news) == news.title.title()


@pytest.mark.django_db
def test_estimate_reading_time():
    news = NewsFactory()

    words_count_title = NewsReadTimeEngine.word_count(news.title)
    words_count_content = NewsReadTimeEngine.word_count(news.content)

    total_time = (
        words_count_title + words_count_content
    ) / NewsReadTimeEngine.WORDS_PER_MINUTE

    tags_count = news.tags.count()

    total_time += (tags_count * NewsReadTimeEngine.SECONDS_PER_TAG) // 60
    total_time = ceil(total_time)

    assert total_time == news.estimated_reading_time
