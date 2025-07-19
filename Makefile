test:
	pytest core/apps/news/tests/ 

cov:
	pytest core/apps/news/ --cov=.  --cov-report html

flake8:
	flake8 .

black:
	black .

isort:
	isort .

runserver:
	python core/manage.py runserver

make-mig:
	python core/manage.py makemigrations

make-super:
	python core/manage.py createsuperuser

migrate:
	python core/manage.py migrate

db:
	sqlite3 db.sqlite3

zoomit:
	python core/manage.py scrape_zoomit