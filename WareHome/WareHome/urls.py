
from django.contrib import admin
from django.urls import path
from .views import HomeView, iniciarSesion, crearCuenta
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('iniciarSesion.html/', iniciarSesion.as_view(), name='iniciarSesion.html'),
    path('iniciarSesion.html/crearCuenta.html/', crearCuenta.as_view(), name='crearCuenta.html')
    
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
