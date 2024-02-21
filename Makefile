init:
	pip install -r requirements.txt

test:
	nosetests tests

exe:
	pyinstaller ./myfaker/main.py
	pyinstaller ./fakerapi/main.py
