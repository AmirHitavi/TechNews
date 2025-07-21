from celery import shared_task
from django.core.management import call_command


@shared_task
def scrape_zoomit():
    call_command(
        "scrape_zoomit",
    )
