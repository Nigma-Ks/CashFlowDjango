from django.contrib import admin
from django.urls import include, path
import operations.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(operations.urls, namespace='operations')),
    path("chaining/", include("smart_selects.urls")),
]
