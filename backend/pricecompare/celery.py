import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pricecompare.settings")

app = Celery("pricecompare")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "refresh-market-prices-every-30-minutes": {
        "task": "apps.core.tasks.refresh_market_prices_task",
        "schedule": 60 * 30,
    }
}
