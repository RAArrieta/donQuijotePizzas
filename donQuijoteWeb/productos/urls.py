from django.urls import path
from . import views

app_name="productos"

urlpatterns = [
    path('', views.home, name='home'),
    path("create/", views.ProductosCreate.as_view(), name="productos_create"),
    path("detail/<int:pk>", views.ProductoDetail.as_view(), name="productos_detail"),
    path("update/<int:pk>", views.ProductoUpdate.as_view(), name="productos_update"),
    path("delete/<int:pk>", views.ProductoDelete.as_view(), name="productos_delete"),
]

urlpatterns += [
    path("categorias/", views.categorias, name="categorias"),
    path("categorias/create/", views.ProductoCategoriaCreate.as_view(), name="categorias_create"),
    path("categorias/update/<int:pk>", views.ProductoCategoriaUpdate.as_view(), name="categorias_update"),
    path("categorias/delete/<int:pk>", views.ProductoCategoriaDelete.as_view(), name="categorias_delete"),   
]

urlpatterns += [
    path("lista_wa", views.lista_wa, name="lista_wa"),
]

