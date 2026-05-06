from django.contrib import admin
from .models import UserProfile, Car, Document, Fine, Reminder

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone']

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['plate', 'brand', 'year', 'color', 'user']
    list_filter = ['user']
    search_fields = ['plate', 'brand', 'user__email']

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['name', 'doc_type', 'car', 'expiry_date', 'remind_days']
    list_filter = ['doc_type', 'car__user']
    search_fields = ['name', 'car__plate']

@admin.register(Fine)
class FineAdmin(admin.ModelAdmin):
    list_display = ['car', 'amount', 'fine_date', 'due_date', 'status']
    list_filter = ['status', 'car__user']
    search_fields = ['reason', 'car__plate']

@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ['user', 'reminder_type', 'message', 'is_seen', 'created_at']
    list_filter = ['is_seen', 'reminder_type']
