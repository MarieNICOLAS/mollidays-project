.PHONY: up down restart migrate createsuperuser logs backend-shell db-shell

up:
	docker-compose up -d --build

down:
	docker-compose down -v

restart:
	docker-compose restart

migrate:
	docker exec -it mollidays-backend python3 manage.py migrate

createsuperuser:
	docker exec -it mollidays-backend python3 manage.py createsuperuser

logs:
	docker-compose logs -f backend

backend-shell:
	docker exec -it mollidays-backend bash

db-shell:
	docker exec -it mollidays-db psql -U myo -d mollidays_db

seed:
	docker exec -w /app -it mollidays-backend python3 scripts/seed_all.py

reset:
	docker-compose down -v
	docker-compose up -d --build
	docker exec -it mollidays-backend python3 manage.py migrate
	docker exec -w /app/ -it mollidays-backend python3 scripts/seed_all.py

