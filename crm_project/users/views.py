from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .forms import CreateUserForm
from django.contrib import messages
from .decorators import allowed_users, unauthenticated_user
from accounts.models import Customer


@unauthenticated_user
def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('accounts:index')
        else:
            messages.info(request, 'Sua senha ou usuário está incorreto')

    return render(request, 'users/login.html')


def logoutuser(request):
    logout(request)
    return redirect('users:loginpage')


@unauthenticated_user
def register(request):
    """Register a new user"""
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            Customer.objects.create(user=user)

            messages.success(request, 'Conta criada com sucesso!')

            return redirect('users:loginpage')

    context = {
        'form': form,
    }
    return render(request, 'users/register.html', context)


@login_required(login_url='users:loginpage')
@allowed_users(allowed_roles=['customer'])
def userpage(request):
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    delivered_orders = orders.filter(status='Delivered').count()
    pending_orders = orders.filter(status='Pending').count()
    context = {
        'orders': orders,
        'total_orders': total_orders,
        'delivered_orders': delivered_orders,
        'pending_orders': pending_orders,
    }
    return render(request, 'users/user.html', context)
