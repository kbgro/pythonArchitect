.EXPORT_ALL_VARIABLES:
FLASK_APP=app.py
FLASK_DEBUG=1
FLASK_ENV=development

test:
	pytest

app:
	flask run --port=15000
