from .env import DEBUG, TOOLBAR, TESTING_MODE

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.gzip.GZipMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
    *(['debug_toolbar.middleware.DebugToolbarMiddleware', ] if DEBUG and TOOLBAR and not TESTING_MODE else []),
]
