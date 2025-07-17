# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


from apps.news.models import News, Tags
from asgiref.sync import sync_to_async
from django.db import IntegrityError

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ScraperPipeline:
    def process_item(self, item, spider):
        return item


class SaveNewsToDjangoPipeLine:

    async def process_item(self, item, spider):
        try:
            await self.save_item(item, spider)
            return item
        except Exception as e:
            spider.logger.error(f"Failed to save item: {e}")
            raise

    @sync_to_async
    def save_item(self, item, spider):
        if News.objects.filter(source=item["source"]).exists():
            spider.logger.info(f"Item already exists: {item['source']}")
            return

        spider.logger.info(f"Creating new news item: {item['source']}")
        news = News.objects.create(
            title=item["title"],
            content=item["content"],
            source=item["source"],
        )

        for tag_title in item["tags"]:
            tag, _ = Tags.objects.get_or_create(title=tag_title)
            news.tags.add(tag)
