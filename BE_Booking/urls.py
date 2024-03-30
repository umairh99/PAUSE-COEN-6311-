from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  
    path('api/', include('registeration_app.urls')),  # Include URLs from registration_app
]
