# Python HTML Generated Loyiha

Bu loyiha Python (Flask) orqali HTML sahifalarni server tomonda generatsiya qiladi.

## Ishga tushirish

```bash
cd python_html_app
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Brauzer: `http://127.0.0.1:5050`

## Deploy (Render - tavsiya)

1. Loyihani GitHub'ga push qiling.
2. Render'da **New + Web Service** tanlang.
3. Repo'ni ulang va quyidagilarni kiriting:
   - Root Directory: `python_html_app`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn -w 2 -k gthread -b 0.0.0.0:$PORT app:app`
4. Environment:
   - `FLASK_DEBUG=0`
5. Deploy bosing.

Yordamchi fayl: `python_html_app/render.yaml`.

## Deploy (Railway/Heroku uslubida)

`Procfile` mavjud:

```text
web: gunicorn -w 2 -k gthread -b 0.0.0.0:$PORT app:app
```

`runtime.txt` ham qo'shilgan (`python-3.11.9`).

## Deploy (Docker)

```bash
cd python_html_app
docker build -t py-html-market .
docker run -p 5050:5050 -e PORT=5050 py-html-market
```

## Sahifalar
- `/` katalog + qidiruv
- `/product/<id>` mahsulot detali
- `/create` yangi mahsulot qo'shish formasi

## Texnologiya
- Python 3
- Flask
- Gunicorn
- Jinja2 templates
- Plain CSS
