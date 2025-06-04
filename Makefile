.PHONY: up down restart migrate createsuperuser logs backend-shell db-shell

up:
	docker-compose up -d --build

down:
	docker-compose down -v

restart:
	docker-compose restart

migrate:
	docker exec -it mollidays-backend python manage.py migrate

createsuperuser:
	docker exec -it mollidays-backend python manage.py createsuperuser

logs:
	docker-compose logs -f backend

backend-shell:
	docker exec -it mollidays-backend bash

db-shell:
	docker exec -it mollidays-db psql -U myo -d mollidays_db
