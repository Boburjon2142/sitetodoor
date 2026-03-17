# Site to door

Qarshi shahri uchun mo'ljallangan, Django templates asosidagi qurilish materiallari marketplace loyihasi.

## Local run

### Windows uchun eng oson usul

```bash
c:\Users\Omen\Desktop\Loyiha\run-python-html.cmd
```

Brauzer: `http://127.0.0.1:5050`

Tekshirish:

```bash
powershell -ExecutionPolicy Bypass -File c:\Users\Omen\Desktop\Loyiha\scripts\check-python-html.ps1
```

To'xtatish:

```bash
c:\Users\Omen\Desktop\Loyiha\stop-python-html.cmd
```

### Qo'lda ishga tushirish

```bash
cd python_html_app
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py seed_marketplace
python manage.py runserver 127.0.0.1:5050 --noreload
```

## PythonAnywhere deploy

1. Repo'ni clone qiling:

```bash
git clone https://github.com/Boburjon2142/sitetodoor.git
cd ~/sitetodoor/python_html_app
```

2. Python 3.10 virtualenv:

```bash
mkvirtualenv --python=/usr/bin/python3.10 sitetodoor-venv
workon sitetodoor-venv
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_marketplace
python manage.py collectstatic --noinput
```

3. Web app konfiguratsiyasi:
- Source code: `/home/<username>/sitetodoor/python_html_app`
- Working directory: `/home/<username>/sitetodoor/python_html_app`
- Virtualenv: `/home/<username>/.virtualenvs/sitetodoor-venv`

4. WSGI fayl:

```python
import os
import sys

path = '/home/<username>/sitetodoor/python_html_app'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

5. Static mapping:
- URL: `/static/`
- Directory: `/home/<username>/sitetodoor/python_html_app/staticfiles`

6. Environment:
- `DEBUG=0`
- `ALLOWED_HOSTS=<username>.pythonanywhere.com`
- `CSRF_TRUSTED_ORIGINS=https://<username>.pythonanywhere.com`
- `SECRET_KEY=<strong-random-secret>`
- `DEMO_ADMIN_PASSWORD=<optional-demo-password>`

7. Reload bosing.

## Deploy yangilash

```bash
cd ~/sitetodoor
git pull origin main
workon sitetodoor-venv
cd ~/sitetodoor/python_html_app
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_marketplace
python manage.py collectstatic --noinput
```

Keyin `Web` tab ichida `Reload` bosing.
