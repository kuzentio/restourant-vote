start:
	docker-compose up

start-in-deamon:
	docker-compose up -d

initDB:
	docker-compose exec web python manage.py init_db_data

create-superuser:
	docker-compose exec web python manage.py createsuperuser

destroy:
	docker-compose down -v
	docker-compose rm -f -s -v

stop:
	docker-compose down

test:
	docker-compose exec web python manage.py test

bash:
	docker-compose exec web bash
