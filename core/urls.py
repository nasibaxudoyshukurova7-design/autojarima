from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', views.profile_view, name='profile'),

    # Cars
    path('cars/', views.car_list, name='car_list'),
    path('cars/add/', views.car_add, name='car_add'),
    path('cars/<int:pk>/', views.car_detail, name='car_detail'),
    path('cars/<int:pk>/edit/', views.car_edit, name='car_edit'),
    path('cars/<int:pk>/delete/', views.car_delete, name='car_delete'),

    # Documents
    path('documents/', views.doc_list, name='doc_list'),
    path('documents/add/<int:car_pk>/', views.doc_add, name='doc_add'),
    path('documents/<int:pk>/edit/', views.doc_edit, name='doc_edit'),
    path('documents/<int:pk>/delete/', views.doc_delete, name='doc_delete'),

    # Fines
    path('fines/', views.fine_list, name='fine_list'),
    path('fines/add/', views.fine_add, name='fine_add'),
    path('fines/<int:pk>/edit/', views.fine_edit, name='fine_edit'),
    path('fines/<int:pk>/delete/', views.fine_delete, name='fine_delete'),
    path('fines/<int:pk>/paid/', views.fine_mark_paid, name='fine_mark_paid'),

    # Reminders
    path('reminders/', views.reminder_list, name='reminder_list'),
    path('reminders/<int:pk>/seen/', views.reminder_seen, name='reminder_seen'),
    path('reminders/seen-all/', views.reminder_seen_all, name='reminder_seen_all'),
]
