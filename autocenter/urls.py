from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from autocenter import settings
from frontend.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
