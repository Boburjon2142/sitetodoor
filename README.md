# SITE-TO-DOOR MVP

Online qurilish materiallari marketplace + delivery platform (MVP).

## Stack
- Backend: Python 3.11+, Django 5, DRF, SimpleJWT, Celery, Redis, PostgreSQL
- Frontend: Next.js App Router, TypeScript, Tailwind
- Infra: Docker Compose

## Monorepo Structure
- `backend/` Django API, admin, seed, tests
- `frontend/` Next.js UI
- `docker-compose.yml` services

## Quick Start
1. `cp .env.example .env`
2. `docker compose up --build`
3. Backend:
   - API: `http://localhost:8000/api/v1/`
   - Swagger: `http://localhost:8000/api/docs/`
   - Admin: `http://localhost:8000/admin/`
4. Frontend: `http://localhost:3000`

## Local (without Docker)
### Backend
1. `cd backend`
2. `python -m venv .venv && .venv\\Scripts\\activate`
3. `pip install -r requirements.txt`
4. `set USE_SQLITE=1` (Windows) or `export USE_SQLITE=1`
5. `python manage.py migrate`
6. `python manage.py runserver`

### Frontend
1. `cd frontend`
2. `npm install`
3. `cp .env.local.example .env.local`
4. `npm run dev`

## Seed Demo Data
- `python manage.py seed_demo_users`
- `python manage.py seed_catalog`

Demo users (phone/password):
- customer: `998900000001` / `customer123`
- supplier: `998900000002` / `supplier123`
- driver: `998900000003` / `driver123`
- admin: `998900000004` / `admin123`

## MVP Flow Demo Script
1. Home page: OTP request + verify (backend console logdagi OTP ni kiriting).
2. Product detail: supplier offers taqqoslash, cartga qo`shish.
3. Checkout: address tanlash/yaratish, to`lov usuli tanlash (`cash` yoki `mockpay`).
4. Orders: holat timeline va mock tracking ko`rish.
5. Driver panel: accept -> location update -> delivered.
6. Supplier panel: offer boshqaruvi.

## API Notes
- Base path: `/api/v1/`
- JWT auth: `Authorization: Bearer <access>`
- OTP throttling: `5/min` per phone+IP
- Webhooks: `/api/v1/payments/webhooks/{provider}/` with idempotency key (`X-Idempotency-Key`)
- Order statuses in code: `preparing`, `on_the_way`, `delivered`
- Uzbek labels: `tayyorlanyapti`, `yo`lda`, `yetkazildi`

## Tests
Critical tests:
- OTP flow
- Cart -> Order checkout
- Payment webhook idempotency
- Delivery status transitions

Run:
- `cd backend`
- `set USE_SQLITE=1` (Windows)
- `python manage.py test`

## Product Decisions
- Cart multi-supplier qo`llab-quvvatlanadi.
- Checkout paytida cart supplier bo`yicha split qilinib alohida orderlarga aylanadi.
- Customer faqat final totalni ko`radi; commission ichki (admin) maydoni sifatida saqlanadi.

## Future Extensions
- Real SMS provider integration
- Real map + live GPS stream
- Payme/Click/Uzum production adapter + signature validation
- Supplier premium placement logic
- Instalment/financing
