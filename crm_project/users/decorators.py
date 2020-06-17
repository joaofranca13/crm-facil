from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_func):
    """Verifies if the user is authenticated, if not the user is
    redirected to the login page"""
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('accounts:index')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def allowed_users(allowed_roles=[]):
    """Verifies if the user has permissons to access the requested url"""
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, *kwargs)
            else:
                return HttpResponse('Não autorizado')
        return wrapper_func
    return decorator


def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'admin':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('users:userpage')

    return wrapper_func
