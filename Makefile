flake8:
	flake8 --ignore=F405 .

black:
	black .

isort:
	isort .

base:
	pip install -r ./requirements/base.txt

local:
	pip install -r ./requirements/local.txt

production:
	pip install -r ./requirements/production.txt

build:
	docker compose up --build -d

up:
	docker compose up 

stop:
	docker compose stop

down:
	docker compose down

down-v:
	docker compose  down -v

logs:
	docker compose logs

api-logs:
	docker compose logs api

db-logs:
	docker compose logs db

worker-logs:
	docker compose logs worker

flower-logs:
	docker compose logs flower

beat-logs:
	docker compose logs beat

status:
	docker ps

shell:
	docker exec -it api bash

makemigrations:
	docker exec api python core/manage.py makemigrations

migrate:
	docker exec api python core/manage.py migrate
	
superuser:
	docker exec -it api python core/manage.py createsuperuser

remove-all:
	docker compose down --rmi all

pytest:
	docker exec -it api pytest core/apps/news/tests/ 

pytest-cov:
	docker exec -it api pytest core/apps/news/tests/  -p no:warnings  --cov=. --cov-report html

zoomit:
	docker exec -it api python core/manage.py scrape_zoomit