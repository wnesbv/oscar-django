
from pathlib import Path
import os
from dotenv import load_dotenv
from oscar.defaults import *


# ...
try:
    from myshop.settings_local import DEBUG, DATABASES, ALLOWED_HOSTS
except ImportError:
    from myshop.host_settings import DEBUG, DATABASES, ALLOWED_HOSTS


BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

load_dotenv(dotenv_path=os.getenv("dotenv_path"))
SECRET_KEY = os.getenv("SECRET_KEY")

ALLOWED_HOSTS_SWITCHING = ALLOWED_HOSTS
DEBUG_SWITCHING = DEBUG

CSRF_COOKIE_SECURE = True
SITE_ID = 2
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"


STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static/"]
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media/"

DISABLE_COLLECTSTATIC = 1


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.contrib.messages.context_processors.messages",
                "oscar.apps.search.context_processors.search_form",
                "oscar.apps.checkout.context_processors.checkout",
                "oscar.apps.communication.notifications.context_processors.notifications",
                "oscar.core.context_processors.metadata",
                "django.template.context_processors.media",
                "django.template.context_processors.static",

            ],
        },
    },
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    # ...
    "django.middleware.http.ConditionalGetMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    # ...
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "oscar.apps.basket.middleware.BasketMiddleware",
    # ...
    "django.contrib.flatpages.middleware.FlatpageFallbackMiddleware",
]

INSTALLED_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "django.contrib.flatpages",
    "oscar.config.Shop",
    "oscar.apps.analytics.apps.AnalyticsConfig",
    "oscar.apps.checkout.apps.CheckoutConfig",
    "oscar.apps.address.apps.AddressConfig",
    "oscar.apps.shipping.apps.ShippingConfig",
    "oscar.apps.catalogue.apps.CatalogueConfig",
    "oscar.apps.catalogue.reviews.apps.CatalogueReviewsConfig",
    "oscar.apps.communication.apps.CommunicationConfig",
    "oscar.apps.partner.apps.PartnerConfig",
    "oscar.apps.basket.apps.BasketConfig",
    "oscar.apps.payment.apps.PaymentConfig",
    "oscar.apps.offer.apps.OfferConfig",
    "oscar.apps.order.apps.OrderConfig",
    "oscar.apps.customer.apps.CustomerConfig",
    "oscar.apps.search.apps.SearchConfig",
    "oscar.apps.voucher.apps.VoucherConfig",
    "oscar.apps.wishlists.apps.WishlistsConfig",
    "oscar.apps.dashboard.apps.DashboardConfig",
    "oscar.apps.dashboard.reports.apps.ReportsDashboardConfig",
    "oscar.apps.dashboard.users.apps.UsersDashboardConfig",
    "oscar.apps.dashboard.orders.apps.OrdersDashboardConfig",
    "oscar.apps.dashboard.catalogue.apps.CatalogueDashboardConfig",
    "oscar.apps.dashboard.offers.apps.OffersDashboardConfig",
    "oscar.apps.dashboard.partners.apps.PartnersDashboardConfig",
    "oscar.apps.dashboard.pages.apps.PagesDashboardConfig",
    "oscar.apps.dashboard.ranges.apps.RangesDashboardConfig",
    "oscar.apps.dashboard.reviews.apps.ReviewsDashboardConfig",
    "oscar.apps.dashboard.vouchers.apps.VouchersDashboardConfig",
    "oscar.apps.dashboard.communications.apps.CommunicationsDashboardConfig",
    "oscar.apps.dashboard.shipping.apps.ShippingDashboardConfig",
    # 3rd-party apps that oscar depends on
    "widget_tweaks",
    "haystack",
    "treebeard",
    "sorl.thumbnail",
    "easy_thumbnails",
    "django_tables2",
    "ckeditor",
    "ckeditor_uploader",
    "flatpage_main",
    "block_page",
    "umessages",
)

AUTHENTICATION_BACKENDS = (
    "oscar.apps.customer.auth_backends.EmailBackend",
    "django.contrib.auth.backends.ModelBackend",
)
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 9,
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
]
LOGIN_REDIRECT_URL = "/"
APPEND_SLASH = True

HAYSTACK_CONNECTIONS = {
    "default": {
        "ENGINE": "haystack.backends.simple_backend.SimpleEngine",
    },
}

ROOT_URLCONF = "myshop.urls"
WSGI_APPLICATION = "myshop.wsgi.application"


# ...
OSCAR_RECENTLY_VIEWED_PRODUCTS = 20
OSCAR_ALLOW_ANON_CHECKOUT = True

OSCAR_INITIAL_ORDER_STATUS = "Pending"
OSCAR_INITIAL_LINE_STATUS = "Pending"

OSCAR_ORDER_STATUS_PIPELINE = {
    "Pending": (
        "Being processed",
        "Cancelled",
    ),
    "Being processed": (
        "Complete",
        "Cancelled",
    ),
    "Cancelled": (),
    "Complete": (),
}

OSCAR_ORDER_STATUS_CASCADE = {
    "Being processed": "Being processed",
    "Cancelled": "Cancelled",
    "Complete": "Shipped",
}



gettext_noop = lambda s: s
LANGUAGES = (
    ("ar", gettext_noop("Arabic")),
    ("ca", gettext_noop("Catalan")),
    ("cs", gettext_noop("Czech")),
    ("da", gettext_noop("Danish")),
    ("de", gettext_noop("German")),
    ("en-gb", gettext_noop("British English")),
    ("el", gettext_noop("Greek")),
    ("es", gettext_noop("Spanish")),
    ("fi", gettext_noop("Finnish")),
    ("fr", gettext_noop("French")),
    ("it", gettext_noop("Italian")),
    ("ko", gettext_noop("Korean")),
    ("nl", gettext_noop("Dutch")),
    ("pl", gettext_noop("Polish")),
    ("pt", gettext_noop("Portuguese")),
    ("pt-br", gettext_noop("Brazilian Portuguese")),
    ("ro", gettext_noop("Romanian")),
    ("ru", gettext_noop("Russian")),
    ("sk", gettext_noop("Slovak")),
    ("uk", gettext_noop("Ukrainian")),
    ("zh-cn", gettext_noop("Simplified Chinese")),
)

TIME_ZONE = "Europe/Minsk"
LANGUAGE_CODE = "en-gb"
USE_I18N = True
USE_L10N = True
USE_TZ = True


# ...
EMAIL_BACKEND = os.getenv("EMAIL_BACKEND")
EMAIL_USE_TLS = True
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = "587"
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")
MANAGERS = (("Siarhei Bloggs", os.getenv("EMAIL_HOST_USER")),)
EMAIL_SUBJECT_PREFIX = "[Oscar myshop]"


# ...
CKEDITOR_JQUERY_URL = "https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"
CKEDITOR_BROWSE_SHOW_DIRS = True
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_UPLOAD_PATH = ""
CKEDITOR_CONFIGS = {
    "default": {
        "removePlugins": "stylesheetparser",
        # "allowedContent": True,
    }
}


DATABASES_SWITCHING = DATABASES

import django_heroku
import dj_database_url

django_heroku.settings(locals())
DATABASES["default"] = dj_database_url.config(
    conn_max_age=600,
    ssl_require=True,
    default=os.getenv("POSTGRESQL_URI"),
)
