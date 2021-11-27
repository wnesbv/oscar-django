from django.views.static import serve
from django.apps import apps
from django.urls import include, path
from django.contrib import admin
from django.conf import settings
from django.contrib.flatpages.sitemaps import FlatPageSitemap
from django.contrib.sitemaps import views
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from oscar.apps.sitemaps import base_sitemaps


urlpatterns = (
    [
        path("i18n/", include("django.conf.urls.i18n")),
        path("admin/", admin.site.urls),
        # ...
        path("umessages", include("umessages.urls")),
        # ...
        path("ckeditor/", include("ckeditor_uploader.urls")),
        # ...
        path("flatpages/", include("django.contrib.flatpages.urls")),

        # ...
        path("sitemap.xml", views.index, {"sitemaps": base_sitemaps}),

        path(
            "sitemap.xml",
            views.sitemap,
            {"sitemaps": {"flatpages": FlatPageSitemap}},
            name="django.contrib.sitemaps.views.sitemap",
        ),
        path(
            "sitemap-<slug:section>.xml",
            views.sitemap,
            {"sitemaps": base_sitemaps},
            name="django.contrib.sitemaps.views.sitemap",
        ),
    ]
    + static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)


urlpatterns += i18n_patterns(
    path("", include(apps.get_app_config("oscar").urls[0])),
)

urlpatterns += [
    path(
        "media/<path:path>",
        serve,
        {
            "document_root": settings.MEDIA_ROOT,
        },
    ),
    path("static/<path:path>", serve, {"document_root": settings.STATIC_ROOT}),
]
