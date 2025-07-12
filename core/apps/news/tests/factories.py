import factory
from autoslug.utils import slugify
from faker import Faker as FakerFactory

from ..models import News, Tags

faker = FakerFactory()


class TagsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tags

    title = factory.LazyAttribute(lambda x: faker.sentence())


class NewsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = News

    title = factory.LazyAttribute(lambda x: faker.sentence())
    content = factory.LazyAttribute(lambda x: faker.paragraph())
    source = factory.LazyAttribute(lambda x: faker.name())
    slug = factory.LazyAttribute(lambda obj: slugify(obj.title))

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return

        for _ in range(5):
            self.tags.add(TagsFactory())
