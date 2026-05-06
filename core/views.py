from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q, Sum
import datetime

from .models import UserProfile, Car, Document, Fine, Reminder
from .forms import RegisterForm, CarForm, DocumentForm, FineForm


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        d = form.cleaned_data
        user = User.objects.create_user(
            username=d['email'],
            email=d['email'],
            password=d['password'],
            first_name=d['first_name'],
            last_name=d['last_name']
        )
        UserProfile.objects.create(user=user, phone=d.get('phone', ''))
        login(request, user)
        messages.success(request, "Muvaffaqiyatli ro'yxatdan o'tdingiz!")
        return redirect('home')
    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    error = None
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            return redirect(request.GET.get('next', 'home'))
        else:
            error = "Email yoki parol noto'g'ri."
    return render(request, 'registration/login.html', {'error': error})


@login_required
def home_view(request):
    user = request.user
    cars = user.cars.all()
    today = datetime.date.today()

    total_fines = Fine.objects.filter(car__user=user)
    unpaid_fines = total_fines.filter(status='unpaid')
    paid_fines = total_fines.filter(status='paid')
    disputed_fines = total_fines.filter(status='disputed')

    unpaid_total = unpaid_fines.aggregate(s=Sum('amount'))['s'] or 0
    paid_total = paid_fines.aggregate(s=Sum('amount'))['s'] or 0

    all_docs = Document.objects.filter(car__user=user)
    expired_docs = [d for d in all_docs if d.days_left < 0]
    warning_docs = [d for d in all_docs if 0 <= d.days_left <= d.remind_days]

    overdue_fines = [f for f in unpaid_fines if f.days_left < 0]
    near_fines = [f for f in unpaid_fines if 0 <= f.days_left <= 7]

    unseen_reminders = Reminder.objects.filter(user=user, is_seen=False)[:5]

    context = {
        'cars': cars,
        'cars_count': cars.count(),
        'total_fines_count': total_fines.count(),
        'unpaid_count': unpaid_fines.count(),
        'paid_count': paid_fines.count(),
        'disputed_count': disputed_fines.count(),
        'unpaid_total': unpaid_total,
        'paid_total': paid_total,
        'expired_docs': expired_docs,
        'warning_docs': warning_docs,
        'overdue_fines': overdue_fines,
        'near_fines': near_fines,
        'unseen_reminders': unseen_reminders,
    }
    return render(request, 'core/home.html', context)


# --- CARS ---
@login_required
def car_list(request):
    cars = request.user.cars.all()
    return render(request, 'core/car_list.html', {'cars': cars})


@login_required
def car_add(request):
    form = CarForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        car = form.save(commit=False)
        car.user = request.user
        car.save()
        messages.success(request, "Avtomobil qo'shildi.")
        return redirect('car_list')
    return render(request, 'core/car_form.html', {'form': form, 'title': "Avtomobil qo'shish"})


@login_required
def car_edit(request, pk):
    car = get_object_or_404(Car, pk=pk, user=request.user)
    form = CarForm(request.POST or None, instance=car)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Avtomobil yangilandi.")
        return redirect('car_list')
    return render(request, 'core/car_form.html', {'form': form, 'title': "Avtomobilni tahrirlash", 'car': car})


@login_required
def car_delete(request, pk):
    car = get_object_or_404(Car, pk=pk, user=request.user)
    if request.method == 'POST':
        car.delete()
        messages.success(request, "Avtomobil o'chirildi.")
        return redirect('car_list')
    return render(request, 'core/confirm_delete.html', {'obj': car, 'type': 'avtomobil'})


@login_required
def car_detail(request, pk):
    car = get_object_or_404(Car, pk=pk, user=request.user)
    docs = car.documents.all()
    fines = car.fines.all()
    unpaid = fines.filter(status='unpaid').aggregate(s=Sum('amount'))['s'] or 0
    paid = fines.filter(status='paid').aggregate(s=Sum('amount'))['s'] or 0
    return render(request, 'core/car_detail.html', {
        'car': car, 'docs': docs, 'fines': fines,
        'unpaid': unpaid, 'paid': paid
    })


# --- DOCUMENTS ---
@login_required
def doc_list(request):
    filter_type = request.GET.get('filter', 'all')
    all_docs = Document.objects.filter(car__user=request.user)

    if filter_type == 'expired':
        docs = [d for d in all_docs if d.days_left < 0]
    elif filter_type == 'warning':
        docs = [d for d in all_docs if 0 <= d.days_left <= d.remind_days]
    elif filter_type == 'ok':
        docs = [d for d in all_docs if d.days_left > d.remind_days]
    else:
        docs = list(all_docs)

    return render(request, 'core/doc_list.html', {'docs': docs, 'filter_type': filter_type})


@login_required
def doc_add(request, car_pk):
    car = get_object_or_404(Car, pk=car_pk, user=request.user)
    form = DocumentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        doc = form.save(commit=False)
        doc.car = car
        doc.save()
        messages.success(request, "Hujjat qo'shildi.")
        return redirect('car_detail', pk=car_pk)
    return render(request, 'core/doc_form.html', {'form': form, 'car': car, 'title': "Hujjat qo'shish"})


@login_required
def doc_edit(request, pk):
    doc = get_object_or_404(Document, pk=pk, car__user=request.user)
    form = DocumentForm(request.POST or None, instance=doc)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Hujjat yangilandi.")
        return redirect('car_detail', pk=doc.car.pk)
    return render(request, 'core/doc_form.html', {'form': form, 'car': doc.car, 'title': "Hujjatni tahrirlash"})


@login_required
def doc_delete(request, pk):
    doc = get_object_or_404(Document, pk=pk, car__user=request.user)
    car_pk = doc.car.pk
    if request.method == 'POST':
        doc.delete()
        messages.success(request, "Hujjat o'chirildi.")
        return redirect('car_detail', pk=car_pk)
    return render(request, 'core/confirm_delete.html', {'obj': doc, 'type': 'hujjat'})


# --- FINES ---
@login_required
def fine_list(request):
    fines = Fine.objects.filter(car__user=request.user)
    status_filter = request.GET.get('status', '')
    car_filter = request.GET.get('car', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    search = request.GET.get('q', '')

    if status_filter:
        fines = fines.filter(status=status_filter)
    if car_filter:
        fines = fines.filter(car__plate__icontains=car_filter)
    if date_from:
        fines = fines.filter(fine_date__gte=date_from)
    if date_to:
        fines = fines.filter(fine_date__lte=date_to)
    if search:
        fines = fines.filter(Q(reason__icontains=search) | Q(car__plate__icontains=search))

    cars = request.user.cars.all()
    return render(request, 'core/fine_list.html', {
        'fines': fines,
        'cars': cars,
        'status_filter': status_filter,
        'car_filter': car_filter,
        'date_from': date_from,
        'date_to': date_to,
        'search': search,
    })


@login_required
def fine_add(request):
    form = FineForm(user=request.user, data=request.POST or None, files=request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Jarima qo'shildi.")
        return redirect('fine_list')
    return render(request, 'core/fine_form.html', {'form': form, 'title': "Jarima qo'shish"})


@login_required
def fine_edit(request, pk):
    fine = get_object_or_404(Fine, pk=pk, car__user=request.user)
    form = FineForm(user=request.user, data=request.POST or None, files=request.FILES or None, instance=fine)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Jarima yangilandi.")
        return redirect('fine_list')
    return render(request, 'core/fine_form.html', {'form': form, 'title': "Jarimani tahrirlash", 'fine': fine})


@login_required
def fine_delete(request, pk):
    fine = get_object_or_404(Fine, pk=pk, car__user=request.user)
    if request.method == 'POST':
        fine.delete()
        messages.success(request, "Jarima o'chirildi.")
        return redirect('fine_list')
    return render(request, 'core/confirm_delete.html', {'obj': fine, 'type': 'jarima'})


@login_required
def fine_mark_paid(request, pk):
    fine = get_object_or_404(Fine, pk=pk, car__user=request.user)
    fine.status = 'paid'
    fine.save()
    # Mark related reminders as seen
    Reminder.objects.filter(user=request.user, fine=fine).update(is_seen=True)
    messages.success(request, "Jarima to'langan deb belgilandi.")
    return redirect('fine_list')


# --- REMINDERS ---
@login_required
def reminder_list(request):
    reminders = Reminder.objects.filter(user=request.user)
    unseen = reminders.filter(is_seen=False)
    seen = reminders.filter(is_seen=True)[:20]
    return render(request, 'core/reminder_list.html', {'unseen': unseen, 'seen': seen})


@login_required
def reminder_seen(request, pk):
    reminder = get_object_or_404(Reminder, pk=pk, user=request.user)
    reminder.is_seen = True
    reminder.save()
    return redirect(request.META.get('HTTP_REFERER', 'reminder_list'))


@login_required
def reminder_seen_all(request):
    Reminder.objects.filter(user=request.user, is_seen=False).update(is_seen=True)
    messages.success(request, "Barcha eslatmalar ko'rildi deb belgilandi.")
    return redirect('reminder_list')


# --- PROFILE ---
@login_required
def profile_view(request):
    user = request.user
    profile, _ = UserProfile.objects.get_or_create(user=user)
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        profile.phone = request.POST.get('phone', profile.phone)
        new_pass = request.POST.get('new_password')
        if new_pass:
            user.set_password(new_pass)
            messages.info(request, "Parol o'zgartirildi. Qayta kiring.")
        user.save()
        profile.save()
        messages.success(request, "Profil yangilandi.")
        return redirect('profile')
    return render(request, 'core/profile.html', {'profile': profile})
