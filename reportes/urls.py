from django.urls import path
from . import views

app_name = 'reportes'

urlpatterns = [
    path('', views.lista_reportes, name='lista'),
    path('nuevo/', views.crear_reporte, name='crear'),
    path('<int:pk>/editar/', views.editar_reporte, name='editar'),
    path('<int:pk>/eliminar/', views.eliminar_reporte, name='eliminar'),
]