# Car Rental Management System - Admin Panel

Faqat admin uchun mo'ljallangan avtomobil ijarasi boshqaruv tizimi Django va Tailwind CSS bilan yaratilgan.

## 🚀 Xususiyatlar

### Asosiy Funksiyalar
- **Admin Panel**: Faqat admin uchun mo'ljallangan
- **Foydalanuvchi boshqaruvi**: Admin orqali foydalanuvchilar qo'shish
- **Mashina boshqaruvi**: Mashinalar ro'yxati, qo'shish, tahrirlash, o'chirish
- **Shartnoma boshqaruvi**: Owner va kompaniya o'rtasidagi shartnomalar
- **Booking boshqaruvi**: Ijara bookinglari va to'lov holati
- **Tizim sozlamalari**: Global parametrlar va konfiguratsiya

### Texnik Xususiyatlar
- **Django 5.2.6** - Backend framework
- **Tailwind CSS** - Zamonaviy va responsive dizayn
- **SQLite** - Ma'lumotlar bazasi (production uchun PostgreSQL tavsiya etiladi)
- **Django Admin** - Ma'lumotlar boshqaruvi
- **Signals** - Avtomatik holat yangilanishi
- **Form validation** - To'liq ma'lumotlar tekshiruvi

## 📋 Tizim Tarkibi

### Modellar
1. **CustomUser** - Foydalanuvchilar (Admin, Owner, Renter)
2. **Vehicle** - Mashinalar (CarMake, CarModel bilan)
3. **Contract** - Shartnomalar (Share/Fixed pricing)
4. **Booking** - Ijara bookinglari
5. **Constant** - Tizim sozlamalari

### Asosiy Qoidalar
- **Plate format**: `12 A 345 BC` (validatsiya bilan)
- **Pricing**: Kunlik va soatlik narxlar
- **Earnings**: Owner va kompaniya daromadlari
- **Status management**: Avtomatik holat yangilanishi
- **Role-based access**: Har bir rol uchun alohida huquqlar

## 🛠️ O'rnatish

### Talablar
- Python 3.8+
- Django 5.2.6
- Virtual environment (tavsiya etiladi)

### O'rnatish qadamlari

1. **Repository ni klon qiling**:
```bash
git clone <repository-url>
cd car-rental-management
```

2. **Virtual environment yarating**:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# yoki
venv\Scripts\activate  # Windows
```

3. **Dependencies o'rnating**:
```bash
pip install django
```

4. **Ma'lumotlar bazasini yarating**:
```bash
python manage.py migrate
```

5. **Superuser yarating**:
```bash
python manage.py createsuperuser
```

6. **Server ishga tushiring**:
```bash
python manage.py runserver
```

7. **Brauzerda oching**: `http://127.0.0.1:8000`

## 👥 Foydalanuvchi Boshqaruvi

### Admin Panel
- **Barcha ma'lumotlarni ko'rish va boshqarish**
- **Foydalanuvchilar qo'shish**: Admin orqali Owner va Renter qo'shish
- **Tizim sozlamalarini o'zgartirish**
- **Booking va shartnoma holatlarini boshqarish**
- **Mashinalar boshqaruvi**
- **To'liq statistika va hisobotlar**

### Foydalanuvchi Qo'shish
- Admin panel orqali yangi foydalanuvchilar qo'shish
- Owner (mashina egasi) va Renter (ijara oluvchi) rollari
- Har bir foydalanuvchi uchun alohida huquqlar

## 🎨 Dizayn

- **Tailwind CSS** - Zamonaviy va responsive dizayn
- **Font Awesome** - Ikonlar
- **Mobile-first** - Barcha qurilmalarda ishlaydi
- **Dark/Light mode** - Foydalanuvchi qulayligi

## 📱 Responsive Dizayn

- **Mobile**: Telefonlar uchun optimallashtirilgan
- **Tablet**: Planshetlar uchun moslashtirilgan
- **Desktop**: Kompyuterlar uchun to'liq funksionallik

## 🔧 Konfiguratsiya

### Environment Variables
```bash
# .env fayl yarating
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///db.sqlite3
```

### Database Settings
Production uchun PostgreSQL tavsiya etiladi:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'car_rental_db',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 🚀 Production Deployment

### Static Files
```bash
python manage.py collectstatic
```

### Database Migration
```bash
python manage.py migrate
```

### Server Configuration
- **Gunicorn** - WSGI server
- **Nginx** - Web server
- **PostgreSQL** - Production database

## 📊 Ma'lumotlar Tahlili

### Dashboard
- Har bir rol uchun alohida dashboard
- Statistika va hisobotlar
- Tezkor amallar

### Reporting
- Owner daromadlari
- Kompaniya daromadlari
- Booking statistikasi

## 🔒 Xavfsizlik

- **Authentication** - Django built-in auth
- **Authorization** - Role-based access control
- **CSRF Protection** - Cross-site request forgery
- **Input Validation** - Form va model validation

## 🧪 Testing

```bash
python manage.py test
```

## 📝 API (Kelajakda)

- REST API yaratish rejasi
- Mobile app uchun API
- Third-party integratsiya

## 🤝 Contributing

1. Fork qiling
2. Feature branch yarating
3. O'zgarishlarni commit qiling
4. Pull request yuboring

## 📄 License

MIT License

## 📞 Support

Muammolar yoki savollar uchun:
- GitHub Issues
- Email: support@example.com

## 🔄 Updates

- **v1.0.0** - Initial release
- **v1.1.0** - API support (planned)
- **v1.2.0** - Mobile app (planned)

---

**E'tibor**: Bu loyiha Django 5.2.6 va Tailwind CSS bilan yaratilgan. Barcha funksiyalar to'liq ishlaydi va production uchun tayyor.
