PORT ?= 8000

install:
	poetry install

dev:
	poetry run flask --app page_analyzer:app run

publish:
	poetry publish --dry-run

lint:
	poetry run flake8 page_analyzer

start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

build:
	./build.sh

roat:
	poetry run gunicorn page_analyzer:app --preload -b 0.0.0.0:1000
	
# gunicorn page_analyzer:app --preload -b 0.0.0.0:1000
# gunicorn app:application --check-config