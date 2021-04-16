from django.utils.deprecation import MiddlewareMixin


# class CustomMiddleware(MiddlewareMixin):
#
#     def process_request(self, request):
#         print()
#         pass
from core.models import LastRequest


class CustomMiddleware(object):
    def __init__(self, get_response):
        """
        One-time configuration and initialisation.
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Code to be executed for each request before the view (and later
        middleware) are called.
        """
        response = self.get_response(request)
        return response

    def process_template_response(self, request, response):
        """
        Called just after the view has finished executing.
        """
        user_id = request.user.id
        if user_id:
            LastRequest.save_activity(request.user.id)
        return response