from django.urls import include, path

from .views import NewsApi, NewsDetailsApi, TagsApi, TagsDetailsApi

urlpatterns = [
    path(
        "tag/",
        include(
            [
                path("", TagsApi.as_view(), name="tag-create-get"),
                path("<uuid:pk>/", TagsDetailsApi.as_view(), name="tag-details"),
            ]
        ),
    ),
    path(
        "news/",
        include(
            [
                path("", NewsApi.as_view(), name="news-create-get"),
                path("<uuid:pk>/", NewsDetailsApi.as_view(), name="news-details"),
            ]
        ),
    ),
]
