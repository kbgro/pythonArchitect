test:
	pytest

app:
	set FLASK_APP=app.py
	set FLASK_DEBUG=1
	set FLASK_ENV=dev
	flask run --port=15000
