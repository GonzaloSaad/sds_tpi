

init: init-venv update-venv init-precommit

init-venv:
	@rm -rf venv
	@python -m venv venv


update-venv:
	@( \
		. venv/bin/activate; \
		poetry update; \
		poetry install; \
	)


init-precommit:
	@echo "Installing pre commit..."
	@( \
		. venv/bin/activate; \
		pre-commit install; \
	)


run:
	@( \
		. venv/bin/activate; \
		uvicorn app.main:app --reload --port 8080; \
	)
