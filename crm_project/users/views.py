from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm, CustomerProfileForm
from django.contrib import messages
from .decorators import users_only, unauthenticated_user


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
    return redirect('loginpage')


@unauthenticated_user
def register(request, **kwargs):
    """Register a new user"""
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')

            messages.success(
                request, 'Conta criada com sucesso, ' + username + "!")

            return redirect('loginpage')

    context = {
        'form': form,
    }
    return render(request, 'users/register.html', context)


@login_required(login_url='loginpage')
@users_only
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


@login_required(login_url='loginpage')
@users_only
def profile(request):
    customer = request.user.customer
    form = CustomerProfileForm(instance=customer)
    if request.method == 'POST':
        form = CustomerProfileForm(
            request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, 'users/profile.html', context)
