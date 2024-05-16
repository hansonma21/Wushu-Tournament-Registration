from django.shortcuts import redirect

class AdminAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'admin' in request.path and not request.user.is_staff:
            return redirect('tourney_pages:home')
        response = self.get_response(request)
        return response