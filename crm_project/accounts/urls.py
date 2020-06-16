from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('', views.index, name='index'),
    path('clientes/<int:pk>', views.customers, name='customers'),
    path('produtos', views.products, name='products'),
    path('criarordem', views.create_order, name='create_order'),
    path('atualizarordem/<int:pk>', views.update_order, name='update_order'),
    path('deletarordem/<int:pk>', views.delete_order, name='delete_order'),
]
