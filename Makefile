.DEFAULT_GOAL := help

.PHONY: help
help:
	@echo "Usage: make [target]"
	@echo "run - Run the application"

.PHONY: run
run:
	@echo "Running the application"
	@pipenv run python manage.py runserver

.PHONY: migrations
migrations:
	@echo "Creating migrations"
	@pipenv run python manage.py makemigrations

.PHONY: migrate
migrate:
	@echo "Applying migrations"
	@pipenv run python manage.py migrate


.PHONY: shell
shell:
	@echo "Running the shell"
	@pipenv run python manage.py shell
