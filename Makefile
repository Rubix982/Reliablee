format:
	autopep8 -r . --in-place

run:
	pipenv run python app.py

del:
	rm -rf ./logs/
