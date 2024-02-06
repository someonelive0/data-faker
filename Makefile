init:
	pip install -r requirements.txt

test:
	nosetests tests

exe:
	pyinstaller 。/faker/main.py
