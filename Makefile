dev:
	uv run uvicorn main:app --reload

lock:
	uv export --no-hashes --format requirements-txt > requirements.txt
