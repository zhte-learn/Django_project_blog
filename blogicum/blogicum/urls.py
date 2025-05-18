from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from .views import UserRegisterView


handler404 = "core.views.page_not_found"
handler500 = "core.views.server_error"

urlpatterns = [
    path(
        "admin/",
        admin.site.urls
    ),
    path(
        "",
        include("blog.urls", namespace="blog")
    ),
    path(
        "pages/",
        include("pages.urls", namespace="pages")
    ),
    path(
        "auth/",
        include("django.contrib.auth.urls")
    ),
    path(
        "auth/registration/",
        UserRegisterView.as_view(),
        name="registration"
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
