from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from FoodBase import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('news/', include('news.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,
                                                                                      document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    from django.conf.urls.static import static

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
