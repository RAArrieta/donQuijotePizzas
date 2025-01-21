from django.urls import path
from . import views

app_name="productos"

urlpatterns = [
    path('', views.home, name='home'),
    path("create/", views.ProductosCreate.as_view(), name="productos_create"),
    path("detail/<int:pk>", views.ProductoDetail.as_view(), name="productos_detail"),
    path("update/<int:pk>", views.ProductoUpdate.as_view(), name="productos_update"),
]

urlpatterns += [
    path("categorias/", views.categorias, name="categorias"),
    path("categorias/create/", views.ProductoCategoriaCreate.as_view(), name="categorias_create"),
    path("categorias/update/<int:pk>", views.ProductoCategoriaUpdate.as_view(), name="categorias_update"),
]

urlpatterns += [
    path("lista_wa", views.lista_wa, name="lista_wa"),
]

