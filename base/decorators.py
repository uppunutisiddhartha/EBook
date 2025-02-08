from django.shortcuts import redirect
from django.contrib import messages
from .models import Student
from functools import wraps

def details_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not Student.objects.filter(user=request.user).exists():
            messages.warning(request, "Please complete your details first.")
            return redirect('base:details')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
