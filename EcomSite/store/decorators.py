from django.http import HttpResponse
from django.shortcuts import redirect


def authenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login')

    return wrapper_func


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('store')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                groups = [group.name for group in request.user.groups.all()]
                for group in groups:
                    if group in allowed_roles:
                        return view_func(request, *args, **kwargs)
                        break
                    else:
                        continue
                else:
                    return HttpResponse('You are not authorised to view this page.')
        return wrapper_func
    return decorator
