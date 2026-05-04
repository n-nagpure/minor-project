from django.utils import timezone

from apps.core.models import PriceHistory, Product, ProductListing
from apps.core.services.adapters import get_platform_adapters


def refresh_product_listings(product: Product) -> int:
    updated_rows = 0
    best_image = product.image_url
    for adapter in get_platform_adapters():
        payload = adapter.fetch_listing(product)
        listing, _ = ProductListing.objects.update_or_create(
            product=product,
            platform=payload["platform"],
            defaults={
                "platform_product_id": payload.get("platform_product_id", ""),
                "title": payload["title"],
                "buy_url": payload["buy_url"],
                "current_price": payload["current_price"],
                "in_stock": payload.get("in_stock", True),
                "last_success_at": timezone.now(),
                "last_error": payload.get("last_error", ""),
            },
        )
        PriceHistory.objects.create(
            listing=listing,
            price=listing.current_price,
            in_stock=listing.in_stock,
        )
        if payload.get("image_url") and not best_image:
            best_image = payload["image_url"]
        updated_rows += 1
    if best_image and best_image != product.image_url:
        product.image_url = best_image
        product.save(update_fields=["image_url"])
    return updated_rows


def refresh_all_product_listings() -> int:
    updated_rows = 0
    for product in Product.objects.all():
        updated_rows += refresh_product_listings(product)
    return updated_rows


def refresh_products_listings(products) -> int:
    updated_rows = 0
    for product in products:
        updated_rows += refresh_product_listings(product)
    return updated_rows
