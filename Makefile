.PHONY: dev test fmt run mlflow index eval

dev:
	python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt

run:
	uvicorn app.server:app --reload --host 0.0.0.0 --port 8000

test:
	pytest -q

mlflow:
	docker compose up mlflow

index:
	python scripts/index_knowledge.py --root data/knowledge

eval:
	python scripts/evaluate.py
