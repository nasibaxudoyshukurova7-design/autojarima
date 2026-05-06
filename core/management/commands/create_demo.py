from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import UserProfile, Car, Document, Fine
import datetime


class Command(BaseCommand):
    help = 'Demo ma\'lumotlarni yaratadi'

    def handle(self, *args, **kwargs):
        # Superuser
        if not User.objects.filter(username='admin').exists():
            su = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write('Superuser yaratildi: admin / admin123')

        # Demo user
        if User.objects.filter(email='test@example.com').exists():
            self.stdout.write('Demo foydalanuvchi allaqachon mavjud.')
            return

        user = User.objects.create_user(
            username='test@example.com',
            email='test@example.com',
            password='test123',
            first_name='Alisher',
            last_name='Karimov'
        )
        UserProfile.objects.create(user=user, phone='+998901234567')

        today = datetime.date.today()

        # Car 1
        car1 = Car.objects.create(user=user, plate='01A123AA', brand='Chevrolet Malibu', year=2021, color='Oq')
        Document.objects.create(
            car=car1, doc_type='sugurta', name='Avtomobil sug\'urtasi',
            issue_date=today - datetime.timedelta(days=335),
            expiry_date=today + datetime.timedelta(days=30),
            remind_days=7
        )
        Document.objects.create(
            car=car1, doc_type='texkorik', name='Texnik ko\'rik',
            issue_date=today - datetime.timedelta(days=300),
            expiry_date=today + datetime.timedelta(days=90),
            remind_days=14
        )

        # Car 2
        car2 = Car.objects.create(user=user, plate='02B456BB', brand='Hyundai Accent', year=2019, color='Kumush')
        Document.objects.create(
            car=car2, doc_type='texpasport', name='Texnik pasport',
            issue_date=today - datetime.timedelta(days=10),
            expiry_date=today + datetime.timedelta(days=5),  # warning zone
            remind_days=7
        )
        Document.objects.create(
            car=car2, doc_type='haydovchi', name='Haydovchilik guvohnomasi',
            issue_date=today - datetime.timedelta(days=1800),
            expiry_date=today + datetime.timedelta(days=200),
            remind_days=30
        )

        # Fines
        Fine.objects.create(
            car=car1, amount=200000, reason='Tezlik oshirish',
            fine_date=today - datetime.timedelta(days=10),
            due_date=today + datetime.timedelta(days=5),  # near deadline
            status='unpaid'
        )
        Fine.objects.create(
            car=car1, amount=100000, reason="Noto'g'ri to'xtash",
            fine_date=today - datetime.timedelta(days=30),
            due_date=today - datetime.timedelta(days=5),
            status='paid'
        )
        Fine.objects.create(
            car=car2, amount=150000, reason='Texnik ko\'rik yo\'qligi',
            fine_date=today - datetime.timedelta(days=5),
            due_date=today + datetime.timedelta(days=25),
            status='disputed'
        )

        self.stdout.write(self.style.SUCCESS(
            'Demo ma\'lumotlar yaratildi!\n'
            'Foydalanuvchi: test@example.com / test123\n'
            'Superuser: admin / admin123'
        ))
