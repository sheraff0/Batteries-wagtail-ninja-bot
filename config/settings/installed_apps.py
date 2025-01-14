from .env import DEBUG, TOOLBAR, TESTING_MODE

INSTALLED_APPS = [
    "apps.root",
    "apps.catalog",
    "apps.journal",
    "apps.sales",
    "apps.stock",
    "apps.finance",
    "apps.menu",
    "ninja",
    "rest_framework.authtoken",
    "search",
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.contrib.search_promotions",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail",
    "modelcluster",
    "taggit",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sitemaps",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    *(["debug_toolbar", ] if DEBUG and TOOLBAR and not TESTING_MODE else []),
]
