from django.db.models import Q
from django_filters import rest_framework as filters


class NewsFilter(filters.FilterSet):
    tags_title = filters.CharFilter(method="get_by_tags_title", label="Tags Title")
    keywords = filters.CharFilter(method="get_by_keywords", label="Keywords")
    excludes = filters.CharFilter(method="get_by_excludes", label="Excludes")

    def get_by_tags_title(self, queryset, name, value):
        if not value:
            return queryset

        tags_title = [tag.strip() for tag in value.split(",") if tag.strip()]

        if not tags_title:
            return queryset.none()

        return queryset.filter(tags__title__in=tags_title).distinct()

    def get_by_keywords(self, queryset, name, value):
        if not value:
            return queryset

        keywords = [keyword.strip() for keyword in value.split(",") if keyword.strip()]

        if not keywords:
            return queryset.none()

        objects = Q()
        for keyword in keywords:
            objects |= Q(content__icontains=keyword) | Q(title__icontains=keyword)

        return queryset.filter(objects).distinct()

    def get_by_excludes(self, queryset, name, value):
        if not value:
            return queryset
        excludes = [exclude.strip() for exclude in value.split(",") if exclude.strip()]

        if not excludes:
            return queryset.none()

        objects = Q()

        for exclude in excludes:
            objects &= ~Q(content__icontains=exclude) & ~Q(title__icontains=exclude)

        return queryset.filter(objects).distinct()
