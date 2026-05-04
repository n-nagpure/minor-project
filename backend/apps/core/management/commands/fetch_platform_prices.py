from django.core.management.base import BaseCommand

from apps.core.services.price_pipeline import refresh_all_product_listings


class Command(BaseCommand):
    help = "Fetch latest platform listings and build price history snapshots."

    def handle(self, *args, **options):
        updated_rows = refresh_all_product_listings()
        self.stdout.write(self.style.SUCCESS(f"Listings refreshed successfully. Rows updated: {updated_rows}"))
