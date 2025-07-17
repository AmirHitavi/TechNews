import os
from pathlib import Path

from django.core.management import BaseCommand
from scrapy import cmdline


class Command(BaseCommand):

    help = "Scrape Zoomit news"

    def handle(self, *args, **kwargs):

        django_path = Path(__file__).resolve().parent.parent.parent.parent.parent
        os.chdir(f"{str(django_path)}/scraper")
        os.system("scrapy crawl zoomit")
