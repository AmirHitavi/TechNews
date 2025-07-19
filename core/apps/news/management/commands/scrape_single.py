import os
from pathlib import Path

from django.core.management import BaseCommand


class Command(BaseCommand):

    help = "Scrape a single Zoomit news by url"

    def add_arguments(self, parser):
        parser.add_argument("url", type=str, help="Zoomit article url")

    def handle(self, *args, **kwargs):
        url = kwargs["url"]

        django_path = Path(__file__).resolve().parent.parent.parent.parent.parent
        os.chdir(f"{str(django_path)}/scraper")
        os.system(f"scrapy crawl zoomit -a custom_url={url}")
