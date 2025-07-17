from scraper.spiders.zoomit import ZoomitSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from django.conf import settings
import os

def scrape_news():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
    settings_module_path = 'config.settings.local'
    os.environ['SCRAPY_SETTINGS_MODULE'] = settings_module_path
    
    process = CrawlerProcess(get_project_settings())
    process.crawl(ZoomitSpider)
    process.start()