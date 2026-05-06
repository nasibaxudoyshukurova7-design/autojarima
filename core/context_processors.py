from .models import Reminder


def reminder_count(request):
    if request.user.is_authenticated:
        count = Reminder.objects.filter(user=request.user, is_seen=False).count()
        return {'unseen_reminders': count}
    return {'unseen_reminders': 0}
