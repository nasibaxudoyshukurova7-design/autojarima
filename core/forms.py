from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Car, Document, Fine


class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=50, label="Ism")
    last_name = forms.CharField(max_length=50, label="Familiya")
    email = forms.EmailField(label="Email")
    phone = forms.CharField(max_length=20, label="Telefon", required=False)
    password = forms.CharField(widget=forms.PasswordInput, label="Parol")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Parolni tasdiqlang")

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Bu email allaqachon ro'yxatdan o'tgan.")
        return email

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password')
        p2 = cleaned.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Parollar mos kelmadi.")
        return cleaned


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['plate', 'brand', 'year', 'color']
        widgets = {
            'plate': forms.TextInput(attrs={'placeholder': '01A123AA', 'class': 'form-control'}),
            'brand': forms.TextInput(attrs={'placeholder': 'Chevrolet Malibu', 'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'min': 1970, 'max': 2030, 'class': 'form-control'}),
            'color': forms.TextInput(attrs={'placeholder': 'Oq', 'class': 'form-control'}),
        }


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['doc_type', 'name', 'issue_date', 'expiry_date', 'remind_days', 'note']
        widgets = {
            'doc_type': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'issue_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'expiry_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'remind_days': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class FineForm(forms.ModelForm):
    class Meta:
        model = Fine
        fields = ['car', 'amount', 'fine_date', 'due_date', 'reason', 'status', 'image', 'note']
        widgets = {
            'car': forms.Select(attrs={'class': 'form-select'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '200000'}),
            'fine_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'reason': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['car'].queryset = Car.objects.filter(user=user)
