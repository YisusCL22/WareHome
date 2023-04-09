
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from productos.urls import productos_urlpatterns

urlpatterns = [
    path('', include('frontend.urls')),
    path('productos/', include(productos_urlpatterns)),
    path('admin/', admin.site.urls),
    path('administrator/', include('administrator.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('registration.urls')),
    
]
