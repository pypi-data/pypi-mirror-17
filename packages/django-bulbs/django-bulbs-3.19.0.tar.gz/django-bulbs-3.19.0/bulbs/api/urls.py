from django.conf import settings
from django.conf.urls import url, include

from bulbs.cms_notifications.api import cms_notifications_view
from .views import api_v1_router, MeViewSet, ReportBugEmail


urlpatterns = (
    url(r"^report-bug/?$", ReportBugEmail.as_view(), name="report-bug"),
    url(r"^me/logout/?$", "django.contrib.auth.views.logout", name="logout"),
    url(r"^me/?$", MeViewSet.as_view({"get": "retrieve"}), name="me"),
    url(r"^", include(api_v1_router.urls))  # noqa
)

if "bulbs.promotion" in settings.INSTALLED_APPS:
    urlpatterns += (
        url(r"^", include("bulbs.promotion.urls")),
    )

if "bulbs.special_coverage" in settings.INSTALLED_APPS:
    urlpatterns += (
        url(r"^", include("bulbs.special_coverage.urls")),
    )

if "bulbs.cms_notifications" in settings.INSTALLED_APPS:
    urlpatterns += (
        url(r"^cms_notifications/(?P<pk>\d+)?", cms_notifications_view, name="cms_notifications"),
    )

if "bulbs.contributions" in settings.INSTALLED_APPS:
    urlpatterns += (
        url(r"^contributions/", include("bulbs.contributions.urls")),
    )

if "bulbs.sections" in settings.INSTALLED_APPS:
    urlpatterns += (
        url(r"^", include("bulbs.sections.urls")),
    )

if "bulbs.poll" in settings.INSTALLED_APPS:
    urlpatterns += (
        url(r"^", include("bulbs.poll.api")),
    )

if "bulbs.super_features" in settings.INSTALLED_APPS:
    urlpatterns += (
        url(r"^", include("bulbs.super_features.api")),
    )


# mparent(2016-08-18): Add new apps here, simpler!
for app in ['bulbs.liveblog']:
    if app in settings.INSTALLED_APPS:
        urlpatterns += (
            url(r"^", include("{}.api".format(app))),
        )
