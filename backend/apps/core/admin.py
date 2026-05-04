from django.contrib import admin

from .models import AccountProfile, EmailVerificationToken, PriceHistory, Product, ProductListing, ProductPrice, WishlistItem

admin.site.register(AccountProfile)
admin.site.register(EmailVerificationToken)
admin.site.register(Product)
admin.site.register(ProductPrice)
admin.site.register(WishlistItem)
admin.site.register(ProductListing)
admin.site.register(PriceHistory)
