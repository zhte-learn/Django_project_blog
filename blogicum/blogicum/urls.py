from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path, reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm


handler404 = "pages.views.page_not_found"
handler500 = "pages.views.server_error"


class UserRegisterView(CreateView):
    template_name = "registration/registration_form.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("login")


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
