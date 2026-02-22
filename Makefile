.PHONY: up down logs migrate makemigrations seed test

up:
	docker compose up --build

down:
	docker compose down

logs:
	docker compose logs -f --tail=200

makemigrations:
	docker compose run --rm backend python manage.py makemigrations

migrate:
	docker compose run --rm backend python manage.py migrate

seed:
	docker compose run --rm backend python manage.py seed_demo_users
	docker compose run --rm backend python manage.py seed_catalog

test:
	docker compose run --rm backend python manage.py test
