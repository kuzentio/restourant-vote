start:
	docker-compose up

initDB:
	docker-compose exec web python manage.py init_db_data

destroy:
	docker-compose down -v
	docker-compose rm -f -s -v

stop:
	docker-compose down

test:
	docker-compose exec web python manage.py test

bash:
	docker-compose exec web bash
