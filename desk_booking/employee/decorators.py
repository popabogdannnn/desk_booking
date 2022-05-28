from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wraper_func(request, *args, **kwargs):
        if (not request.user.is_authenticated):
            return redirect('login')
        else:
            return view_func(request, *args, **kwargs)
    return wraper_func