from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_zonas, name='inicio'),
    path('zonas/', views.listar_zonas, name='zonas_listado'),
    path('zonas/<int:zona_id>/', views.detalle_zona, name='zona_detalle'),
    path('resumen-zonas/', views.resumen_zonas, name='resumen_zonas'),
]