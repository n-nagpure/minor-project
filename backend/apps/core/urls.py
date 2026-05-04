from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    SignupView,
    UserProfileView,
    WishlistViewSet,
    compare_search_view,
    dashboard_view,
    login_view,
    logout_view,
    verify_email_view,
)

router = DefaultRouter()
router.register("wishlist", WishlistViewSet, basename="wishlist")

urlpatterns = [
    path("auth/signup/", SignupView.as_view(), name="signup"),
    path("auth/verify-email/", verify_email_view, name="verify-email"),
    path("auth/login/", login_view, name="login"),
    path("auth/logout/", logout_view, name="logout"),
    path("products/compare/", compare_search_view, name="product-compare"),
    path("dashboard/", dashboard_view, name="dashboard"),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("", include(router.urls)),
]
