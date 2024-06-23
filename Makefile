clean:
	@find . -name "*.pyc" | xargs rm -rf
	@find . -name "*.pyo" | xargs rm -rf
	@find . -name "*.log" | xargs rm -rf
	@find . -name "__pycache__" -type d | xargs rm -rf
	@find . -name ".pytest_cache" -type d | xargs rm -rf
	@rm -f .coverage
	@rm -rf htmlcov/
	@rm -f coverage.xml
	@rm -f *.log
	@rm -f celerybeat-schedule.bak
	@rm -f celerybeat-schedule.dat
	@rm -f celerybeat-schedule.dir
	@rm -f celerybeat-schedule
	@rm -f celerybeat-schedule.db

build-venv:
	python3.12 -m venv venv

install-git-hooks:
	@pip install pre-commit
	@pre-commit install

install-dependencies:
	@pip install -r requirements.txt
	@pip install --upgrade pip

migrate-up:
	mongodb-migrate --url mongodb://localhost:27017/dbaas-db --migrations migrations
	@echo "✅ Migrações aplicadas"

docker-compose:
	docker-compose up -d
	make migrate-up

load-test-env:
	@cp devtools/dotenv.test .env

load-dev-env:
	@cp devtools/dotenv.dev .env

run-dbaas-api:
	@uvicorn dbaas.api:app --host 0.0.0.0 --port 8000 --reload

run-dbaas-worker:
	@celery -A dbaas.configs.celery.celery worker --loglevel=INFO -Ofair --without-mingle --without-gossip --without-heartbeat -Q dbaas.provision.vm.1

run-dbaas-beat:
	@celery -A dbaas.configs.celery.celery beat --loglevel=INFO

run-computexaas-api:
	@uvicorn computexaas_api.api:app --host 0.0.0.0 --port 8001 --reload

bandit:
	bandit -r -f custom dbaas,computexaas_api

isort:
	@isort --py auto -m 3 --tc --up -l 120 .

isort-check:
	@isort -c --py auto -m 3 --tc --up  -l 120 .

black:
	@black --config black.toml .

black-check:
	@black --config black.toml --check .

flake8:
	@flake8 --config flake8.ini

dead-fixture:
	@pytest --dead-fixtures

lint: clean isort black flake8 bandit

lint-check: isort-check black-check  bandit flake8 dead-fixture

test: load-test-env
	pytest -p no:warnings

coverage: clean load-test-env
	@py.test -p no:warnings --cov=dbaas --cov=computexaas_api --cov-report=term-missing --cov-fail-under=90 ./test/