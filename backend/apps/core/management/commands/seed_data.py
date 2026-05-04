from django.core.management.base import BaseCommand

from django.utils import timezone

from apps.core.models import PriceHistory, Product, ProductListing, ProductPrice


class Command(BaseCommand):
    help = "Seed sample products and platform prices."

    def handle(self, *args, **options):
        products = [
            {
                "name": "Apple iPhone 15",
                "model_number": "A3090",
                "brand": "Apple",
                "category": "Smartphone",
                "image_url": "https://via.placeholder.com/120",
                "prices": [
                    ("amazon", 71999, "https://www.amazon.in/Apple-iPhone-15-128-GB/dp/B0CHX1W1XY"),
                    ("flipkart", 70999, "https://www.flipkart.com/apple-iphone-15-black-128-gb/p/itm6ac6485515ae4"),
                    ("croma", 72490, "https://www.croma.com/apple-iphone-15-128gb-black-/p/300684"),
                ],
            },
            {
                "name": "Samsung Galaxy S24",
                "model_number": "SM-S921B",
                "brand": "Samsung",
                "category": "Smartphone",
                "image_url": "https://via.placeholder.com/120",
                "prices": [
                    ("amazon", 64999, "https://www.amazon.in/Samsung-Galaxy-S24-5G-Smartphone/dp/B0CS5TK8YX"),
                    ("flipkart", 63999, "https://www.flipkart.com/samsung-galaxy-s24-onyx-black-256-gb/p/itm0453f57deea4e"),
                    ("reliance", 65499, "https://www.reliancedigital.in/samsung-galaxy-s24-5g-256-gb-8-gb-ram-onyx-black-mobile-phone/p/494267608"),
                ],
            },
        ]

        for item in products:
            price_rows = item.pop("prices")
            product, _ = Product.objects.get_or_create(model_number=item["model_number"], defaults=item)
            for source, price, buy_url in price_rows:
                ProductPrice.objects.update_or_create(
                    product=product,
                    source=source,
                    defaults={"price": price, "buy_url": buy_url, "in_stock": True},
                )
                listing, _ = ProductListing.objects.update_or_create(
                    product=product,
                    platform=source,
                    defaults={
                        "platform_product_id": product.model_number,
                        "title": product.name,
                        "buy_url": buy_url,
                        "current_price": price,
                        "in_stock": True,
                        "last_success_at": timezone.now(),
                        "last_error": "",
                    },
                )
                PriceHistory.objects.create(listing=listing, price=price, in_stock=True)

        self.stdout.write(self.style.SUCCESS("Sample data inserted."))
