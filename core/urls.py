from django.contrib import admin
from django.urls import path, include

admin.site.site_header = "Homeventory Admin"
admin.site.site_title = "Homeventory Admin Portal"
admin.site.index_title = "Welcome to Homeventory Portal"

urlpatterns = [
    # Authentication endpoints from dj-rest-auth
    path("api/auth/", include("dj_rest_auth.urls")),
    path("api/auth/registration/", include("dj_rest_auth.registration.urls")),
    # Admin
    path("admin/", admin.site.urls),
]
