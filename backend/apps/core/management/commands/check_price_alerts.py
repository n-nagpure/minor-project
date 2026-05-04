from decimal import Decimal

from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.db.models import Min

from apps.core.models import WishlistItem


class Command(BaseCommand):
    help = "Send email alerts when wishlist product drops below target price."

    def handle(self, *args, **options):
        alerts_sent = 0
        items = WishlistItem.objects.filter(notify_on_drop=True, target_price__isnull=False).select_related("user", "product")

        for item in items:
            min_price = item.product.listings.aggregate(min_price=Min("current_price"))["min_price"]
            if min_price is None:
                min_price = item.product.prices.aggregate(min_price=Min("price"))["min_price"]
            if min_price is None:
                continue

            if Decimal(min_price) <= item.target_price:
                send_mail(
                    subject=f"Price drop alert: {item.product.name}",
                    message=(
                        f"Good news! {item.product.name} ({item.product.model_number}) is now at INR {min_price}.\n"
                        f"Your target price was INR {item.target_price}."
                    ),
                    from_email=None,
                    recipient_list=[item.user.email],
                    fail_silently=True,
                )
                alerts_sent += 1

        self.stdout.write(self.style.SUCCESS(f"Price alert check completed. Emails sent: {alerts_sent}"))
