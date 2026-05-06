from .utils import check_reminders


class ReminderMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and not request.path.startswith('/admin/'):
            try:
                check_reminders(request.user)
            except Exception:
                pass
        return self.get_response(request)
