init:
	pip install -r requirements.txt

test:
	nosetests tests

exe:
	pyinstaller ./fake_data/main.py
	pyinstaller ./fake_api/main.py
