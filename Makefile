init-env:
	python3 -m venv env
act-env:
	. env/bin/activate
i:
	pip install --upgrade pip && pip install -r requirements.txt
mig:
	make migration && make migrate
cru:
	python manage.py createsuperuser
test:
	python3 manage.py test
run-asgi:
	uvicorn core.asgi:application --host 0.0.0.0 --port 1026 --reload
run:
	python manage.py runserver 0.0.0.0:1026

#others
git-rm-idea:
	git rm -r --cached .idea/
collect:
	python manage.py collectstatic --noinput
rm-static:
	rm -rf staticfiles/
migration:
	python3 manage.py makemigrations
migrate:
	python3 manage.py migrate
startapp:
	python manage.py startapp $(name) && mv $(name) apps/v1/$(name)
clear-linux:
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete && find . -path "*/migrations/*.pyc"  -delete
clear-windows:
	Get-ChildItem -Path "*\migrations\0*.py" | Remove-Item -Force
	Get-ChildItem -Path "*\migrations\*.pyc" | Remove-Item -Force
no-sqlite-db:
	rm -rf db.sqlite3
re-django:
	pip3 uninstall Django -y && pip3 install Django
no-venv:
	rm -rf env/ venv/ .venv/
re-mig:
	make no-sqlite-db && make clear-linux && make re-django & make i && make mig && make cru && make collect && make test && make run-asgi
run-wsgi:
	gunicorn core.wsgi:application --bind 0.0.0.0:1026
tunnel:
	jprq http 1026 -s goride-api
open-bash:
	sudo docker exec -it goride_api bash
down:
	sudo docker compose down -v
up:
	sudo docker compose up --build
logs:
	sudo docker compose logs
restart:
	sudo docker rm -f goride_api goride_nginx goride_redis & make down & make up
seed_languages:
	python manage.py seed_languages