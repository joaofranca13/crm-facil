from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def loginpage(request):
    if request.user.is_authenticated:
        return redirect('accounts:index')
    else:
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


@login_required(login_url='login')
def logoutuser(request):
    logout(request)
    return redirect('users:loginpage')


def register(request):
    """Register a new user"""
    if request.user.is_authenticated:
        return redirect('accounts:index')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Conta criada com sucesso!')
                return redirect('users:loginpage')

        context = {
            'form': form,
        }
        return render(request, 'users/register.html', context)
