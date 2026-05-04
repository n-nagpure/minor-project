import re
import uuid
from datetime import timedelta

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Count
from django.db.models import Q
from django.utils import timezone
from rest_framework import generics, permissions, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from django.conf import settings

from .models import AccountProfile, EmailVerificationToken, Product, WishlistItem
from .serializers import ProductSerializer, SignupSerializer, UserProfileSerializer, WishlistItemSerializer
from .services.price_pipeline import refresh_products_listings


class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = SignupSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "detail": "Account created. Check your email and click the verification link before logging in.",
            },
            status=status.HTTP_201_CREATED,
        )


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def verify_email_view(request):
    token_str = request.query_params.get("token", "").strip()
    if not token_str:
        return Response({"detail": "Verification token is missing."}, status=status.HTTP_400_BAD_REQUEST)
    try:
        token_uuid = uuid.UUID(str(token_str))
    except ValueError:
        return Response({"detail": "Invalid verification token."}, status=status.HTTP_400_BAD_REQUEST)

    token_obj = EmailVerificationToken.objects.filter(token=token_uuid).select_related("user").first()
    if not token_obj:
        return Response({"detail": "Invalid or already used verification link."}, status=status.HTTP_400_BAD_REQUEST)

    max_age = timedelta(hours=settings.EMAIL_VERIFICATION_TOKEN_HOURS)
    if timezone.now() - token_obj.created_at > max_age:
        return Response({"detail": "This verification link has expired. Please sign up again or contact support."}, status=status.HTTP_400_BAD_REQUEST)

    user = token_obj.user
    profile, _ = AccountProfile.objects.get_or_create(user=user, defaults={"email_verified": False})
    profile.email_verified = True
    profile.save(update_fields=["email_verified"])
    EmailVerificationToken.objects.filter(user=user).delete()
    return Response({"detail": "Email verified successfully. You can log in now."})


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def login_view(request):
    login_identifier = (request.data.get("username") or "").strip()
    password = request.data.get("password")

    # Attempt normal authentication first.
    user = authenticate(username=login_identifier, password=password)

    # Fallback to case-insensitive username lookup or email login.
    if not user and login_identifier:
        user_lookup = User.objects.filter(username__iexact=login_identifier).first()
        if not user_lookup and "@" in login_identifier:
            user_lookup = User.objects.filter(email__iexact=login_identifier).first()
        if user_lookup:
            user = authenticate(username=user_lookup.username, password=password)

    if not user:
        return Response({"detail": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)
    try:
        profile = user.account_profile
    except AccountProfile.DoesNotExist:
        AccountProfile.objects.create(user=user, email_verified=True)
    else:
        if not profile.email_verified:
            return Response(
                {"detail": "Please verify your email before logging in. Check your inbox for the verification link."},
                status=status.HTTP_400_BAD_REQUEST,
            )
    token, _ = Token.objects.get_or_create(user=user)
    return Response({
        "token": token.key, 
        "username": user.username, 
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email
    })


@api_view(["POST"])
def logout_view(request):
    if request.auth:
        request.auth.delete()
    return Response({"detail": "Logged out successfully."})


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def compare_search_view(request):
    query = request.query_params.get("q", "").strip()
    products_qs = Product.objects.prefetch_related("prices", "listings")
    if query:
        products_qs = products_qs.filter(Q(model_number__icontains=query) | Q(name__icontains=query))
        if not products_qs.exists() and len(query) >= 3:
            normalized = re.sub(r"[^A-Za-z0-9]+", "-", query).strip("-").upper()[:90] or "SEARCH"
            dynamic_product, _ = Product.objects.get_or_create(
                model_number=f"QRY-{normalized}",
                defaults={
                    "name": query,
                    "brand": "Unknown",
                    "category": "General",
                },
            )
            products_qs = Product.objects.filter(id=dynamic_product.id).prefetch_related("prices", "listings")
        matched_products = list(products_qs[:10])
        if matched_products:
            refresh_products_listings(matched_products)
        products_qs = Product.objects.prefetch_related("prices", "listings").filter(
            Q(model_number__icontains=query) | Q(name__icontains=query)
        )
    serializer = ProductSerializer(products_qs[:20], many=True)
    return Response(serializer.data)


@api_view(["GET"])
def dashboard_view(request):
    wishlist_count = WishlistItem.objects.filter(user=request.user).count()
    compared_products = (
        WishlistItem.objects.filter(user=request.user)
        .values("product")
        .aggregate(unique_products=Count("product", distinct=True))
    )
    return Response(
        {
            "username": request.user.username,
            "first_name": request.user.first_name or "",
            "last_name": request.user.last_name or "",
            "wishlist_count": wishlist_count,
            "compared_products": compared_products["unique_products"],
        }
    )


class WishlistViewSet(viewsets.ModelViewSet):
    serializer_class = WishlistItemSerializer

    def get_queryset(self):
        return WishlistItem.objects.filter(user=self.request.user).select_related("product").prefetch_related("product__prices")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
