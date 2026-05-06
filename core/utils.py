import datetime
from .models import Document, Fine, Reminder


def check_reminders(user):
    today = datetime.date.today()

    # Check documents
    cars = user.cars.all()
    for car in cars:
        for doc in car.documents.all():
            days_left = (doc.expiry_date - today).days
            if days_left <= doc.remind_days:
                # Check if reminder already exists
                existing = Reminder.objects.filter(
                    user=user,
                    document=doc,
                    is_seen=False
                ).exists()
                if not existing:
                    if days_left < 0:
                        msg = f"⚠️ {car.plate} - {doc.get_doc_type_display()} muddati {abs(days_left)} kun oldin o'tib ketgan!"
                    elif days_left == 0:
                        msg = f"🔴 {car.plate} - {doc.get_doc_type_display()} muddati BUGUN tugaydi!"
                    else:
                        msg = f"🟡 {car.plate} - {doc.get_doc_type_display()} muddati {days_left} kunda tugaydi."
                    Reminder.objects.create(
                        user=user,
                        reminder_type='document',
                        document=doc,
                        message=msg
                    )

    # Check fines
    for car in cars:
        for fine in car.fines.filter(status='unpaid'):
            days_left = (fine.due_date - today).days
            if days_left <= 7:
                existing = Reminder.objects.filter(
                    user=user,
                    fine=fine,
                    is_seen=False
                ).exists()
                if not existing:
                    if days_left < 0:
                        msg = f"⚠️ {car.plate} - {fine.reason} jarimasi to'lov muddati {abs(days_left)} kun oldin o'tib ketgan! ({fine.amount:,} so'm)"
                    elif days_left == 0:
                        msg = f"🔴 {car.plate} - {fine.reason} jarimasi to'lov muddati BUGUN tugaydi! ({fine.amount:,} so'm)"
                    else:
                        msg = f"🟡 {car.plate} - {fine.reason} jarima to'lov muddati {days_left} kunda tugaydi. ({fine.amount:,} so'm)"
                    Reminder.objects.create(
                        user=user,
                        reminder_type='fine',
                        fine=fine,
                        message=msg
                    )
