from django.http import HttpResponseForbidden
from functools import wraps

def role_required(required_role):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and getattr(request.user, 'role', None) == required_role:
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("You are not authorized to view this page.")
        return _wrapped_view
    return decorator
