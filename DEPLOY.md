# Render.com'ga Deploy Qilish

## Qisqa versiya (5 daqiqa)

1. **GitHub'ga push qiling:**
   ```bash
   git add .
   git commit -m "Production setup"
   git push origin main
   ```

2. **Render.com'ga kiring:**
   - https://render.com ga o'ting
   - GitHub bilan login qiling

3. **Yangi Web Service yarating:**
   - "New +" → "Web Service"
   - GitHub repo tanlang (`school-platform`)
   - **Build Command:** `pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - **Start Command:** `daphne -b 0.0.0.0 -p $PORT school_platform.asgi:application`
   - **Plan:** Free

4. **Environment Variables qo'shish:**
   Dashboard → Settings → Environment Variables:
   ```
   DEBUG = False
   SECRET_KEY = (o'zingiz kerakli long string)
   ALLOWED_HOSTS = yourapp.onrender.com
   ```

5. **Database qo'shish:**
   - Settings → Create Database
   - PostgreSQL (free)
   - DATABASE_URL avtomatik tuziladi

6. **Deploy qilish:**
   - "Deploy" tugmasi bosing
   - 2–3 daqiqa kutib, sayt ochiladi
   - URL: `https://yourapp.onrender.com`

---

## Muammolar va yechimlari

### ❌ "Python version mismatch"
**Yechim:** Render'da `python-version` faylini yarating:
```
3.11
```

### ❌ "Static files not found"
**Yechim:** `collectstatic` buildda ishga tushgani tekshiring.

### ❌ "Database connection error"
**Yechim:** DATABASE_URL environment variable'ni tekshiring.
```bash
render logs
```

---

## Link

Sayt burada ochiladi:
```
https://yourapp-name.onrender.com
```

Boshqalar shu link'ni kiritsa, saytga kirishadi va foydalanuvchi bo'lishi mumkin.

---

**Ishlab chiqish rejimida** (localhost'da):
```bash
.venv\Scripts\python.exe manage.py runserver
```
