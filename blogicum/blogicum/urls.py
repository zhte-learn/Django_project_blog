from django.contrib import admin
from django.urls import include, path

# handler404 = 'core.views.page_not_found'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls', namespace='blog')),
    path('pages/', include('pages.urls', namespace="pages")),
    path('auth/', include('django.contrib.auth.urls')),
    
]
