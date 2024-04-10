from django.shortcuts import redirect
from .models import User

path_to_protect = [
    "/home/",
    "/update/",
    "/articles/",
    "/experts/",
    "/marks/",
]

forbidden_expert = [
    'articles/add/',
    'articles/<int:pk>/update/',
    'experts/add/',
    'experts/<int:pk>/update/',
]

forbidden_worker = [
    'articles/<int:pk>/mark/',
    'marks/'
]

class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info
        for pref in path_to_protect:
            if path.startswith(pref):
                if not request.user.is_authenticated:
                    return redirect('/login/')
        response = self.get_response(request)
        return response
    
class RoleCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        path = request.path_info
        if path.startswith('/login/')  or path.startswith('/admin/'):
            return response

        try:
            role = User.objects.get(username=request.user.username).role
        except User.DoesNotExist:
            return redirect('/login/')

        if request.user.is_authenticated:
            match role:
                case User.EXPERT:
                    forbidden_urls = forbidden_expert
                case User.WORKER:
                    forbidden_urls = forbidden_worker
                case User.NONE:
                    return redirect('/access_denied/')
                case _:
                    forbidden_urls = []

            if request.path in forbidden_urls:
                return redirect('/access_denied/')

        return response