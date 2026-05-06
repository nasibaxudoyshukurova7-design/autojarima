from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.user.email})"


class Car(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cars')
    plate = models.CharField(max_length=20, verbose_name="Davlat raqami")
    brand = models.CharField(max_length=100, verbose_name="Marka/Model")
    year = models.IntegerField(verbose_name="Yili")
    color = models.CharField(max_length=50, verbose_name="Rang")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.plate} - {self.brand} ({self.year})"

    class Meta:
        ordering = ['-created_at']


class Document(models.Model):
    DOC_TYPES = [
        ('texpasport', 'Texnik pasport'),
        ('texkorik', 'Texnik ko\'rik'),
        ('sugurta', 'Avtomobil sug\'urtasi'),
        ('haydovchi', 'Haydovchilik guvohnomasi'),
        ('other', 'Boshqa'),
    ]

    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='documents')
    doc_type = models.CharField(max_length=20, choices=DOC_TYPES, verbose_name="Hujjat turi")
    name = models.CharField(max_length=200, verbose_name="Hujjat nomi")
    issue_date = models.DateField(verbose_name="Berilgan sana")
    expiry_date = models.DateField(verbose_name="Amal qilish muddati")
    remind_days = models.IntegerField(default=7, verbose_name="Necha kun oldin eslatish")
    note = models.TextField(blank=True, verbose_name="Izoh")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_doc_type_display()} - {self.car.plate}"

    @property
    def days_left(self):
        today = datetime.date.today()
        delta = self.expiry_date - today
        return delta.days

    @property
    def status(self):
        d = self.days_left
        if d < 0:
            return 'expired'
        elif d <= self.remind_days:
            return 'warning'
        else:
            return 'ok'

    class Meta:
        ordering = ['expiry_date']


class Fine(models.Model):
    STATUS_CHOICES = [
        ('unpaid', "To'lanmagan"),
        ('paid', "To'langan"),
        ('disputed', "E'tiroz bildirilgan"),
    ]

    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='fines')
    amount = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="Jarima miqdori (so'm)")
    fine_date = models.DateField(verbose_name="Jarima sanasi")
    due_date = models.DateField(verbose_name="To'lov muddati")
    reason = models.CharField(max_length=300, verbose_name="Jarima sababi")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='unpaid', verbose_name="Holati")
    image = models.ImageField(upload_to='fines/', blank=True, null=True, verbose_name="Rasm/Hujjat")
    note = models.TextField(blank=True, verbose_name="Izoh")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.car.plate} - {self.amount} so'm ({self.get_status_display()})"

    @property
    def days_left(self):
        today = datetime.date.today()
        delta = self.due_date - today
        return delta.days

    @property
    def is_overdue(self):
        return self.status == 'unpaid' and self.days_left < 0

    class Meta:
        ordering = ['-fine_date']


class Reminder(models.Model):
    TYPE_CHOICES = [
        ('document', 'Hujjat muddati'),
        ('fine', 'Jarima to\'lov muddati'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reminders')
    reminder_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    document = models.ForeignKey(Document, on_delete=models.CASCADE, null=True, blank=True)
    fine = models.ForeignKey(Fine, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    is_seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.message[:50]}"

    class Meta:
        ordering = ['-created_at']
