# AutoJarima – Avtomobil jarimalari va hujjatlar monitoringi

## O'rnatish va ishga tushirish

### 1. Virtual muhit (tavsiya etiladi)
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### 2. Kutubxonalarni o'rnatish
```bash
pip install -r requirements.txt
```

### 3. Ma'lumotlar bazasini tayyorlash
```bash
python manage.py migrate
```

### 4. Demo ma'lumotlarni yaratish
```bash
python manage.py create_demo
```
Bu buyruq quyidagilarni yaratadi:
- Demo foydalanuvchi: `test@example.com` / `test123`
- Superuser (admin panel): `admin` / `admin123`
- 2 ta avtomobil, 4 ta hujjat, 3 ta jarima

### 5. Serverni ishga tushirish
```bash
python manage.py runserver
```

### 6. Brauzerda ochish
- Asosiy sayt: http://127.0.0.1:8000/
- Admin panel: http://127.0.0.1:8000/admin/

## Asosiy funksiyalar

- **Foydalanuvchi tizimi** – Ro'yxatdan o'tish, kirish, profil
- **Avtomobillar** – Qo'shish, tahrirlash, o'chirish
- **Hujjatlar** – Texpasport, texko'rik, sug'urta, haydovchilik guvohnomasi monitoringi
- **Jarimalar** – Qo'lda kiritish, holat boshqaruvi, filtr va qidiruv
- **Eslatmalar** – Muddat yaqinlashganda avtomatik eslatma
- **Statistika** – Bosh sahifada to'liq hisobot

## Texnologiyalar
- Django 4.2
- Bootstrap 5
- SQLite (lokal baza)
- Pillow (rasm yuklash)
