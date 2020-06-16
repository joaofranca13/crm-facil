from django.forms import ModelForm
from .models import Order


class OrderForm(ModelForm):
    """Create new orders in the Order Model"""
    class Meta:
        model = Order
        fields = '__all__'
