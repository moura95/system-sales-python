.PHONY: db-up
db-up:
	docker-compose up -d midas_sales_db

.PHONY: db-down
db-down:
	docker-compose down --volumes && docker volume prune -f
	docker-compose up -d midas_sales_db
	rm -rf alembic/versions/*
	sleep 10
	psql "postgresql://postgres:postgres@localhost:5431/midas_sales" -f db/migrations/drop.sql
	poetry run alembic revision --autogenerate -m "init"
	poetry run alembic upgrade head
	psql "postgresql://postgres:postgres@localhost:5431/midas_sales" -f db/populate.sql

.PHONY: create-migration
create-migration:
	@read -p "Por favor, forneça o nome da migração: " Nome; \
	if [ -z "$$Nome" ]; then \
		Nome="migrate"; \
	fi; \
	poetry run alembic revision --autogenerate -m "$$Nome"

.PHONY: migrate
migrate:
	poetry run alembic upgrade head

.PHONY: rollback
rollback:
	@read -p "Por favor, forneça o número de migrações ou enter para base: " N; \
	N=$${N:-"base"}; \
	poetry run alembic downgrade $$N

.PHONY: celery
celery:
	celery -A midas_sales.tasks worker --loglevel=info
