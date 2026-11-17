dev:
	docker compose -f compose.yaml -f compose.dev.yaml up --build -d

dev-down:
	docker compose -f compose.yaml -f compose.dev.yaml down

prod:
	docker compose -f compose.yaml -f compose.prod.yaml up --build -d

prod-down:
	docker compose -f compose.yaml -f compose.prod.yaml down

logs:
	docker compose -f compose.yaml -f compose.dev.yaml logs -f

migrate:
	docker compose -f compose.yaml -f compose.dev.yaml exec backend python manage.py migrate

createsuperuser:
	docker compose -f compose.yaml -f compose.dev.yaml exec backend python manage.py createsuperuser