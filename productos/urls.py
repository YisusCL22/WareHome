from django.urls import path
from . import views
from django.urls import path
#from productos import views #importará los métodos que generemos en nuestra app productoss
from django.views.decorators.csrf import csrf_exempt
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

productos_urlpatterns = [
    path('productos_main/',views.productos_main,name="productos_main"),
    path('productos_local_add/',views.productos_local_add,name="productos_local_add"),
    path('productos_local_save/',views.productos_local_save,name="productos_local_save"),
    path('productos_local_ver/<local_id>/',views.productos_local_ver,name="productos_local_ver"),
    path('productos_list_locales/',views.productos_list_locales,name="productos_list_locales"),

    path('productos_local_carga_masiva/',views.productos_local_carga_masiva,name="productos_local_carga_masiva"),
    path('productos_local_carga_masiva_save/',views.productos_local_carga_masiva_save,name="productos_local_carga_masiva_save"),
    path('import_file/',views.import_file,name="import_file"),

    #endPoints
    path('productos_local_add_rest/', views.productos_local_add_rest),  
    path('productos_local_list_rest/', views.productos_local_list_rest),  
    path('productos_local_get_element_rest/', views.productos_local_get_element_rest),  
    path('productos_local_update_element_rest/', views.productos_local_update_element_rest), 
    path('productos_local_del_element_rest/', views.productos_local_del_element_rest), 
    path('productos_local_list_date_rest/', views.productos_local_list_date_rest), 
    path('productos_local_list_range_date_rest/', views.productos_local_list_range_date_rest), 
    path('productos_local_list_contains/', views.productos_local_list_contains), 

    #path("product_list_rest/",views.product_list_rest),
    #path("product_edit_rest/",views.product_edit_rest),
    
    ]