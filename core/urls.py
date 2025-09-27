from django.contrib import admin
from django.urls import path, include

admin.site.site_header = "Homeventory Admin"
admin.site.site_title = "Homeventory Admin Portal"
admin.site.index_title = "Welcome to Homeventory Portal"

urlpatterns = [
    path("api-auth/", include("rest_framework.urls")),
    # Admin
    path("admin/", admin.site.urls),
]
