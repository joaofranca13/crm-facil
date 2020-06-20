from django.shortcuts import render, redirect
from .models import Customer, Product, Tag, Order
from .forms import OrderForm
from django.forms import inlineformset_factory
from .filters import OrderFilter
from django.contrib.auth.decorators import login_required
from users.decorators import allowed_users, admin_only


@login_required(login_url='loginpage')
@admin_only
def index(request):
    """Creates the home page with the dashboard"""
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_customers = customers.count()
    total_orders = orders.count()
    delivered_orders = orders.filter(status='Delivered').count()
    pending_orders = orders.filter(status='Pending').count()
    context = {
        'orders': orders,
        'customers': customers,
        'total_customers': total_customers,
        'total_orders': total_orders,
        'delivered_orders': delivered_orders,
        'pending_orders': pending_orders,
    }

    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='loginpage')
@admin_only
def products(request):
    """Exihibts all the created products"""
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'accounts/products.html', context)


@login_required(login_url='loginpage')
@admin_only
def customers(request, pk):
    """Display the customer detail page"""
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    total_orders = orders.count()
    my_filter = OrderFilter(request.GET, queryset=orders)
    orders = my_filter.qs
    context = {
        'customer': customer,
        'orders': orders,
        'total_orders': total_orders,
        'my_filter': my_filter,
    }

    return render(request, 'accounts/customers.html', context)


@login_required(login_url='loginpage')
@admin_only
def create_order(request, pk):
    """View for creating new orders"""
    orderformset = inlineformset_factory(
        Customer, Order, fields=('product', 'status'), extra=4)
    customer = Customer.objects.get(id=pk)
    formset = orderformset(queryset=Order.objects.none(), instance=customer)
    if request.method == 'POST':
        formset = orderformset(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {
        'form': formset,
    }
    return render(request, 'accounts/form_order.html', context)


@login_required(login_url='loginpage')
@admin_only
def update_order(request, pk):
    """View for updating existing orders"""
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {
        'form': form,
    }
    return render(request, 'accounts/form_order.html', context)


@login_required(login_url='loginpage')
@admin_only
def delete_order(request, pk):
    """View for deleting existing orders"""
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('/')

    context = {
        'item': order,
    }
    return render(request, 'accounts/delete_ordem.html', context)
