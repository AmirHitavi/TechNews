from django_filters.rest_framework.backends import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .filters import NewsFilter
from .models import News, Tags
from .serializers import (
    NewsCreateInputSerializer,
    NewsDetailsInputSerializer,
    NewsDetailsOutputSerializer,
    NewsOutputSerializer,
    TagDetailsOutputSerializer,
    TagInputSerializer,
    TagOutputSerializer,
)


class TagsApi(GenericAPIView):
    serializer_class = TagOutputSerializer

    def get_queryset(self):
        return Tags.objects.all()

    def get_serializer(self, *args, **kwargs):
        if self.request.method == "POST":
            return TagInputSerializer(*args, **kwargs)
        else:
            return TagOutputSerializer(*args, **kwargs)

    @swagger_auto_schema(
        request_body=TagInputSerializer, responses={201: TagOutputSerializer}
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        tag = Tags.objects.create(title=serializer.validated_data.get("title"))
        return Response(
            TagOutputSerializer(tag, context={"request": request}).data,
            status=status.HTTP_201_CREATED,
        )

    @swagger_auto_schema(responses={200: TagOutputSerializer})
    def get(self, request):
        tags = self.get_queryset()
        paginate_tags = self.paginate_queryset(tags)
        serializer = self.get_serializer(paginate_tags, many=True)
        return self.get_paginated_response(serializer.data)


class TagsDetailsApi(GenericAPIView):
    serializer_class = TagDetailsOutputSerializer
    lookup_field = "pk"

    def get_queryset(self):
        return Tags.objects.all()

    def get_serializer(self, *args, **kwargs):
        if self.request.method == "PUT":
            return TagInputSerializer(*args, **kwargs)
        return TagDetailsOutputSerializer(*args, **kwargs)

    @swagger_auto_schema(responses={200: TagDetailsOutputSerializer})
    def get(self, request, pk):
        try:
            tag = self.get_object()
            serializer = self.get_serializer(tag)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Tags.DoesNotExist:
            raise NotFound(detail="tag item not found")

    @swagger_auto_schema(
        request_body=TagInputSerializer, responses={204: TagDetailsOutputSerializer}
    )
    def put(self, request, pk):
        try:
            tag = self.get_object()
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            tag.title = serializer.validated_data.get("title")
            tag.save()

            return Response(
                TagDetailsOutputSerializer(tag).data, status=status.HTTP_204_NO_CONTENT
            )
        except Tags.DoesNotExist:
            raise NotFound(detail="tag item not found")

    @swagger_auto_schema(responses={204: "No content"})
    def delete(self, request, pk):
        try:
            tag = self.get_object()
            tag.delete()
            return Response("No content", status=status.HTTP_204_NO_CONTENT)
        except Tags.DoesNotExist:
            raise NotFound(detail="tag item not found")


class NewsApi(GenericAPIView):
    serializer_class = NewsOutputSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_class = NewsFilter

    def get_queryset(self):
        return News.objects.all()

    def get_serializer(self, *args, **kwargs):
        if self.request.method == "POST":
            return NewsCreateInputSerializer(*args, **kwargs)
        else:
            return NewsOutputSerializer(*args, **kwargs)

    @swagger_auto_schema(
        request_body=NewsCreateInputSerializer, responses={201: NewsOutputSerializer}
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        news = News.objects.create(
            title=data.get("title"),
            content=data.get("content"),
            source=data.get("source"),
            is_public=data.get("is_public"),
        )
        for tag in data.get("tags"):
            try:
                news.tags.add(Tags.objects.get(title=tag))
            except Tags.DoesNotExist:
                raise NotFound(detail=f"{tag} tag item not exists.")

        return Response(
            NewsOutputSerializer(news, context={"request": request}).data,
            status=status.HTTP_201_CREATED,
        )

    @swagger_auto_schema(
        responses={200: TagOutputSerializer},
        manual_parameters=[
            openapi.Parameter(
                name="tags_title",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Comma-separated tag titles filter",
            ),
            openapi.Parameter(
                name="keywords",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Comma-separated keywords filter for title and content",
            ),
            openapi.Parameter(
                name="excludes",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Comma-separated keyword exclude for title and content",
            ),
        ],
    )
    def get(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        paginate_news = self.paginate_queryset(queryset)
        serializer = self.get_serializer(paginate_news, many=True)
        return self.get_paginated_response(serializer.data)


class NewsDetailsApi(GenericAPIView):
    serializer_class = NewsDetailsOutputSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return News.objects.all()

    def get_serializer(self, *args, **kwargs):
        if self.request.method == "PUT":
            return NewsDetailsInputSerializer(*args, **kwargs)
        return NewsDetailsOutputSerializer(*args, **kwargs)

    @swagger_auto_schema(responses={200: NewsDetailsOutputSerializer})
    def get(self, request, slug):
        try:
            news = self.get_object()
            serializer = self.get_serializer(news)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Tags.DoesNotExist:
            raise NotFound(detail="tag item not found")

    @swagger_auto_schema(
        request_body=NewsDetailsInputSerializer,
        responses={204: NewsDetailsOutputSerializer},
    )
    def put(self, request, slug):
        try:
            news = self.get_object()
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            data = serializer.validated_data

            if data.get("title") is not None:
                news.title = data.get("title")

            if data.get("content") is not None:
                news.content = data.get("content")

            if data.get("source") is not None:
                news.source = data.get("source")

            if data.get("tags") == []:
                pass
            else:
                news.tags.clear()
                for tag in data.get("tags"):
                    try:
                        news.tags.add(Tags.objects.get(title=tag))
                    except Tags.DoesNotExist:
                        raise NotFound(detail=f"{tag} tag item not exists.")

            if data.get("is_public") is not None:
                news.is_public = data.get("is_public")

            news.save()

            return Response(
                TagDetailsOutputSerializer(news).data, status=status.HTTP_204_NO_CONTENT
            )
        except Tags.DoesNotExist:
            raise NotFound(detail="tag item not found")

    @swagger_auto_schema(responses={204: "No content"})
    def delete(self, request, slug):
        try:
            news = self.get_object()
            news.delete()
            return Response("No content", status=status.HTTP_204_NO_CONTENT)
        except Tags.DoesNotExist:
            raise NotFound(detail="tag item not found")
