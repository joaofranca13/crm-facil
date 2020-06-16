import django_filters
from django_filters import DateFilter
from .models import Customer, Product, Order, Tag


class OrderFilter(django_filters.FilterSet):
    """Creates a multiparameter filter"""
    start_date = DateFilter(field_name='date_created',
                            lookup_expr='gte', label='Criado após')
    end_date = DateFilter(field_name='date_created',
                          lookup_expr='lte', label='Antes de')

    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['customer', 'date_created']
