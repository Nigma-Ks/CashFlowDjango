from django.contrib import admin
from django.urls import include, path
import operations.urls
import catalog.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(operations.urls, namespace='operations')),
    path('catalog/', include(catalog.urls, namespace='catalog'))
]
