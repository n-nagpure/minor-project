from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.mail import send_mail
from django.utils import timezone
from rest_framework import serializers

from .models import AccountProfile, EmailVerificationToken, Product, ProductListing, ProductPrice, WishlistItem


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, min_length=8)
    first_name = serializers.CharField(required=True, min_length=1, max_length=30)
    last_name = serializers.CharField(required=True, min_length=1, max_length=30)

    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email", "password", "confirm_password")

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        return attrs

    def validate_first_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("First name is required.")
        if not value.replace(" ", "").isalpha():
            raise serializers.ValidationError("First name should contain only letters and spaces.")
        return value.title()

    def validate_last_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Last name is required.")
        if not value.replace(" ", "").isalpha():
            raise serializers.ValidationError("Last name should contain only letters and spaces.")
        return value.title()

    def validate_password(self, value):
        if not any(ch.isupper() for ch in value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        if not any(ch.islower() for ch in value):
            raise serializers.ValidationError("Password must contain at least one lowercase letter.")
        if not any(ch.isdigit() for ch in value):
            raise serializers.ValidationError("Password must contain at least one number.")
        if value.isalnum():
            raise serializers.ValidationError("Password must contain at least one special character.")
        validate_password(value)
        return value

    def create(self, validated_data):
        # Remove confirm_password as it's not needed for user creation
        validated_data.pop('confirm_password', None)
        
        validated_data["username"] = validated_data["username"].strip().lower()
        validated_data["email"] = validated_data["email"].strip().lower()
        validated_data["first_name"] = validated_data["first_name"].strip().title()
        validated_data["last_name"] = validated_data["last_name"].strip().title()
        
        user = User.objects.create_user(**validated_data)
        AccountProfile.objects.create(user=user, email_verified=False)
        token = EmailVerificationToken.objects.create(user=user)
        verify_path = f"/#/verify-email?token={token.token}"
        verify_link = f"{settings.FRONTEND_BASE_URL.rstrip('/')}{verify_path}"
        try:
            send_mail(
                subject="Verify your email — Price Comparison",
                message=(
                    f"Click to verify your account:\n{verify_link}\n\n"
                    f"This link expires in {settings.EMAIL_VERIFICATION_TOKEN_HOURS} hours."
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
        except Exception as exc:
            EmailVerificationToken.objects.filter(user=user).delete()
            user.delete()
            raise serializers.ValidationError(
                {"detail": f"Verification email could not be sent. Check EMAIL_* settings. ({exc})"}
            ) from exc
        return user


class ProductPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPrice
        fields = ("id", "source", "price", "buy_url", "in_stock", "fetched_at")


class ProductSerializer(serializers.ModelSerializer):
    prices = serializers.SerializerMethodField()
    lowest_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ("id", "name", "model_number", "brand", "image_url", "category", "lowest_price", "prices")

    def get_lowest_price(self, obj):
        listing_min_price = (
            obj.listings.filter(current_price__gt=0, last_error="")
            .order_by("current_price")
            .values_list("current_price", flat=True)
            .first()
        )
        return listing_min_price

    def get_prices(self, obj):
        listings = list(obj.listings.all())
        if listings:
            return [
                {
                    "id": row.id,
                    "source": row.platform,
                    "price": str(row.current_price) if row.current_price > 0 else None,
                    "buy_url": row.buy_url,
                    "in_stock": row.in_stock,
                    "fetched_at": row.fetched_at,
                    "status_message": row.last_error or "Live",
                }
                for row in listings
            ]
        return [
            {
                "id": row.id,
                "source": row.source,
                "price": None,
                "buy_url": row.buy_url,
                "in_stock": row.in_stock,
                "fetched_at": row.fetched_at,
                "status_message": "Seed data only. Live price not fetched yet.",
            }
            for row in obj.prices.all()
        ]


class WishlistItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(source="product", queryset=Product.objects.all(), write_only=True)

    class Meta:
        model = WishlistItem
        fields = ("id", "product", "product_id", "target_price", "notify_on_drop", "created_at")


class UserProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    new_password = serializers.CharField(write_only=True, required=False, allow_blank=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, required=False, allow_blank=True, min_length=8)

    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email", "new_password", "confirm_password")
        read_only_fields = ("id",)

    def validate_username(self, value):
        user = self.instance
        value = value.strip().lower()
        if User.objects.exclude(id=user.id).filter(username__iexact=value).exists():
            raise serializers.ValidationError("This username is already in use.")
        return value

    def validate_email(self, value):
        user = self.instance
        value = value.strip().lower()
        if User.objects.exclude(id=user.id).filter(email__iexact=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

    def validate_new_password(self, value):
        if not value:
            return value
        if not any(ch.isupper() for ch in value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        if not any(ch.islower() for ch in value):
            raise serializers.ValidationError("Password must contain at least one lowercase letter.")
        if not any(ch.isdigit() for ch in value):
            raise serializers.ValidationError("Password must contain at least one number.")
        if value.isalnum():
            raise serializers.ValidationError("Password must contain at least one special character.")
        validate_password(value, self.instance)
        return value

    def update(self, instance, validated_data):
        new_password = validated_data.pop("new_password", "")
        confirm_password = validated_data.pop("confirm_password", "")
        if "first_name" in validated_data:
            instance.first_name = validated_data.get("first_name", instance.first_name)
        if "last_name" in validated_data:
            instance.last_name = validated_data.get("last_name", instance.last_name)
        if "username" in validated_data:
            instance.username = validated_data.get("username", instance.username)
        if "email" in validated_data:
            instance.email = validated_data.get("email", instance.email)
        if new_password:
            if new_password != confirm_password:
                raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
            instance.set_password(new_password)
        instance.save()
        return instance
