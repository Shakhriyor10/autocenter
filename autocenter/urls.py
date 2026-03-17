from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from autocenter import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('frontend.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)