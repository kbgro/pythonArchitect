.EXPORT_ALL_VARIABLES:
FLASK_APP=app.py
FLASK_DEBUG=1
FLASK_ENV=development

test:
	pytest

e2e:
	pytest tests/e2e/test_external_events.py

app:
	flask run --port=15000
