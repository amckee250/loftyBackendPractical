from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from lofty_backend_practical_proj import settings

urlpatterns = [
    path('__debug__/', include('debug_toolbar.urls')),
    path('admin/', admin.site.urls),
    path('items/', include('key_lookup.urls')),
    path('dogs/', include('verified_puppers.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)