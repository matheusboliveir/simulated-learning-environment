.PHONY: up up-ollama down migration build rebuild tables

up:
	docker compose --profile gemini up -d

build:
	docker compose --profile gemini --profile ollama build

rebuild:
	docker compose --profile gemini --profile ollama build --no-cache

up-ollama:
	docker compose --profile ollama up -d

down:
	docker compose down

migration:
	@test -n "$(MESSAGE)" || { echo '❌ Informe MESSAGE. Exemplo: make migration MESSAGE="create snapshots"'; exit 1; }
	@APP_SERVICE=$$(docker compose ps --status running --services | grep -E '^app(-gemini|-ollama)?$$' | head -n 1); \
	if [ -z "$$APP_SERVICE" ]; then \
		echo "❌ Nenhum container da aplicação está rodando."; \
		exit 1; \
	fi; \
	echo "🔍 Aplicação encontrada: $$APP_SERVICE"; \
	echo "1️⃣ Gerando a migration..."; \
	docker compose exec "$$APP_SERVICE" uv run alembic revision --autogenerate -m "$(MESSAGE)"; \
	echo "2️⃣ Aplicando a migration..."; \
	docker compose exec "$$APP_SERVICE" uv run alembic upgrade head

tables:
	docker compose exec db sh -c 'psql -U "$$POSTGRES_USER" -d "$$POSTGRES_DB" -c "\dt"'