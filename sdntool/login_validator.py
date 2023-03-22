from functools import wraps

from django.shortcuts import redirect


def login_check(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.session.get('login'):
            return function(request, *args, **kwargs)
        else:
            return redirect('login')

    return wrap