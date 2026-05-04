from __future__ import annotations

import re
from decimal import Decimal
from urllib.parse import quote_plus, urljoin, urlparse

import requests
from apps.core.models import Product


class BasePlatformAdapter:
    platform = "base"
    default_url = ""
    search_url_template = ""

    def fetch_listing(self, product: Product) -> dict:
        raise NotImplementedError

    def _get_seed_row(self, product: Product):
        return product.prices.filter(source=self.platform).first()

    def _fallback_price(self, product: Product) -> Decimal:
        listing_row = product.listings.filter(platform=self.platform).first()
        if listing_row:
            return Decimal(listing_row.current_price)
        seed_row = self._get_seed_row(product)
        return Decimal(seed_row.price) if seed_row else Decimal("0.00")

    def _fallback_url(self, product: Product) -> str:
        listing_row = product.listings.filter(platform=self.platform).first()
        if listing_row and listing_row.buy_url:
            return listing_row.buy_url
        seed_row = self._get_seed_row(product)
        return seed_row.buy_url if seed_row else ""

    def _build_search_url(self, product: Product) -> str:
        query = quote_plus(f"{product.name} {product.model_number}".strip())
        if self.search_url_template:
            return self.search_url_template.format(query=query)
        return self.default_url

    def _fetch_html(self, url: str) -> str:
        response = requests.get(
            url,
            timeout=12,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0 Safari/537.36"
                ),
                "Accept-Language": "en-IN,en;q=0.9",
            },
        )
        response.raise_for_status()
        return response.text

    def _is_unavailable_page(self, html: str) -> bool:
        markers = [
            "product not found",
            "page not found",
            "sorry, this page is not available",
            "no results found",
        ]
        body = html.lower()
        return any(marker in body for marker in markers)

    def _extract_price(self, html: str) -> Decimal | None:
        patterns = [
            r'"priceToPay"\s*:\s*\{"amount"\s*:\s*([0-9][0-9,]*\.?[0-9]*)',
            r'"finalPrice"\s*:\s*"?(?:₹)?\s*([0-9][0-9,]*\.?[0-9]*)"?',
            r'"discountedPrice"\s*:\s*"?(?:₹)?\s*([0-9][0-9,]*\.?[0-9]*)"?',
            r'"price"\s*:\s*"([0-9][0-9,]*\.?[0-9]*)"',
            r'"current_price"\s*:\s*"([0-9][0-9,]*\.?[0-9]*)"',
            r'"sellingPrice"\s*:\s*"?([0-9][0-9,]*\.?[0-9]*)"?',
            r'<meta[^>]+property="product:price:amount"[^>]+content="([0-9][0-9,]*\.?[0-9]*)"',
        ]
        for pattern in patterns:
            match = re.search(pattern, html, flags=re.IGNORECASE)
            if not match:
                continue
            try:
                return Decimal(match.group(1).replace(",", ""))
            except Exception:
                continue
        return None

    def _extract_title(self, html: str, fallback: str) -> str:
        og_match = re.search(r'<meta\s+property="og:title"\s+content="([^"]+)"', html, flags=re.IGNORECASE)
        if og_match:
            return og_match.group(1).strip()
        title_match = re.search(r"<title>(.*?)</title>", html, flags=re.IGNORECASE | re.DOTALL)
        if title_match:
            return re.sub(r"\s+", " ", title_match.group(1)).strip()
        return fallback

    def _extract_image_url(self, html: str, fallback: str) -> str:
        og_image = re.search(r'<meta\s+property="og:image"\s+content="([^"]+)"', html, flags=re.IGNORECASE)
        if og_image:
            return og_image.group(1).strip()
        img_src = re.search(r'<img[^>]+src="(https?://[^"]+)"', html, flags=re.IGNORECASE)
        if img_src:
            return img_src.group(1).strip()
        return fallback

    def _extract_first_product_url_from_search(self, html: str) -> str:
        return ""

    def _clean_error_message(self, exc: Exception, context: str = "fetch") -> str:
        error_text = str(exc).lower()
        if "403" in error_text:
            return "Blocked by platform (403)."
        if "404" in error_text:
            return "Product page not found (404)."
        if "timeout" in error_text:
            return "Platform request timed out."
        if "connection" in error_text:
            return "Unable to connect to platform."
        if context == "search":
            return "Unable to fetch platform search results."
        return "Unable to verify live price right now."

    def _product_id_from_url(self, url: str, fallback: str) -> str:
        path = urlparse(url).path.strip("/")
        if not path:
            return fallback
        return path.split("/")[-1] or fallback

    def _build_listing(self, product: Product) -> dict:
        fallback_price = self._fallback_price(product)
        buy_url = self._fallback_url(product)

        if not buy_url:
            search_url = self._build_search_url(product)
            try:
                search_html = self._fetch_html(search_url)
                first_product_url = self._extract_first_product_url_from_search(search_html)
                if first_product_url:
                    buy_url = first_product_url
                else:
                    return {
                        "platform": self.platform,
                        "platform_product_id": product.model_number,
                        "title": product.name,
                        "buy_url": "",
                        "current_price": Decimal("0.00"),
                        "in_stock": False,
                        "last_error": "No direct product link found on platform search.",
                        "image_url": product.image_url,
                    }
            except Exception as exc:
                return {
                    "platform": self.platform,
                    "platform_product_id": product.model_number,
                    "title": product.name,
                    "buy_url": "",
                    "current_price": Decimal("0.00"),
                    "in_stock": False,
                    "last_error": self._clean_error_message(exc, context="search"),
                    "image_url": product.image_url,
                }

        try:
            html = self._fetch_html(buy_url)
            if self._is_unavailable_page(html):
                return {
                    "platform": self.platform,
                    "platform_product_id": product.model_number,
                    "title": product.name,
                    "buy_url": "",
                    "current_price": Decimal("0.00"),
                    "in_stock": False,
                    "last_error": "Direct product page unavailable.",
                    "image_url": product.image_url,
                }
            parsed_price = self._extract_price(html)
            parsed_title = self._extract_title(html, product.name)
            parsed_image = self._extract_image_url(html, product.image_url)
            if parsed_price is None:
                return {
                    "platform": self.platform,
                    "platform_product_id": self._product_id_from_url(buy_url, product.model_number),
                    "title": parsed_title,
                    "buy_url": buy_url,
                    "current_price": Decimal("0.00"),
                    "in_stock": True,
                    "last_error": "Live page found, but current price could not be verified.",
                    "image_url": parsed_image,
                }
            return {
                "platform": self.platform,
                "platform_product_id": self._product_id_from_url(buy_url, product.model_number),
                "title": parsed_title,
                "buy_url": buy_url,
                "current_price": parsed_price,
                "in_stock": True,
                "last_error": "",
                "image_url": parsed_image,
            }
        except Exception as exc:
            return {
                "platform": self.platform,
                "platform_product_id": product.model_number,
                "title": product.name,
                "buy_url": buy_url,
                "current_price": Decimal("0.00"),
                "in_stock": False,
                "last_error": self._clean_error_message(exc),
                "image_url": product.image_url,
            }


class AmazonAdapter(BasePlatformAdapter):
    platform = "amazon"
    default_url = "https://www.amazon.in/"
    search_url_template = "https://www.amazon.in/s?k={query}"

    def fetch_listing(self, product: Product) -> dict:
        return self._build_listing(product)

    def _extract_first_product_url_from_search(self, html: str) -> str:
        patterns = [r'href="(/[^"]*/dp/[A-Z0-9]{10}[^"]*)"', r'href="(/dp/[A-Z0-9]{10}[^"]*)"']
        for pattern in patterns:
            match = re.search(pattern, html, flags=re.IGNORECASE)
            if match:
                return urljoin(self.default_url, match.group(1).replace("&amp;", "&"))
        return ""


class FlipkartAdapter(BasePlatformAdapter):
    platform = "flipkart"
    default_url = "https://www.flipkart.com/"
    search_url_template = "https://www.flipkart.com/search?q={query}"

    def fetch_listing(self, product: Product) -> dict:
        return self._build_listing(product)

    def _extract_first_product_url_from_search(self, html: str) -> str:
        patterns = [r'href="(/[^"]+/p/[^"]+)"', r'href="(/[^"]*itm[a-z0-9]+[^"]*)"']
        for pattern in patterns:
            match = re.search(pattern, html, flags=re.IGNORECASE)
            if match:
                return urljoin(self.default_url, match.group(1).replace("&amp;", "&"))
        return ""


class CromaAdapter(BasePlatformAdapter):
    platform = "croma"
    default_url = "https://www.croma.com/"
    search_url_template = "https://www.croma.com/searchB?q={query}"

    def fetch_listing(self, product: Product) -> dict:
        return self._build_listing(product)

    def _extract_first_product_url_from_search(self, html: str) -> str:
        match = re.search(r'href="(/[^"]+/p/[0-9]+)"', html, flags=re.IGNORECASE)
        if match:
            return urljoin(self.default_url, match.group(1).replace("&amp;", "&"))
        return ""


class RelianceAdapter(BasePlatformAdapter):
    platform = "reliance"
    default_url = "https://www.reliancedigital.in/"
    search_url_template = "https://www.reliancedigital.in/search?q={query}"

    def fetch_listing(self, product: Product) -> dict:
        return self._build_listing(product)

    def _extract_first_product_url_from_search(self, html: str) -> str:
        match = re.search(r'href="(/[^"]+/p/[0-9]+)"', html, flags=re.IGNORECASE)
        if match:
            return urljoin(self.default_url, match.group(1).replace("&amp;", "&"))
        return ""


def get_platform_adapters() -> list[BasePlatformAdapter]:
    return [AmazonAdapter(), FlipkartAdapter(), CromaAdapter(), RelianceAdapter()]
