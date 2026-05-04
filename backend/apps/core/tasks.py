from celery import shared_task

from apps.core.services.price_pipeline import refresh_all_product_listings


@shared_task
def refresh_market_prices_task() -> int:
    return refresh_all_product_listings()
