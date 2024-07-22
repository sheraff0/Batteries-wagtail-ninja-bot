from django.conf import settings
from django.urls import include, path
from django.contrib import admin

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.contrib.sitemaps.views import sitemap

from api.main import app as api

from search import views as search_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("catalog/", include("apps.catalog.urls")),
    path("journal/", include("apps.journal.urls")),
    path("reports/", include("apps.reports.urls")),
    path("api/", api.urls),
]


if not settings.S3_STORAGE:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = urlpatterns + [
    path('sitemap.xml', sitemap),
    path("админ/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("search/", search_views.search, name="search"),
    path("", include(wagtail_urls)),
]

# Debug toolbar
if settings.DEBUG and settings.TOOLBAR and not settings.TESTING_MODE:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls)), *urlpatterns]
