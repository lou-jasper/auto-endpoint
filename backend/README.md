uvicorn app.main:app --reload

celery -A app.core.celery_app.celery_app worker --loglevel=INFO
